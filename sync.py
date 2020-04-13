# -*- coding: utf-8 -*-
import json
import logging

from lingualeo import Lingualeo
from kindle import KindleV5


def sync(db_file="vocab.db"):
    log = logging.getLogger()
    kdb = KindleV5(db_file)
    kindle_dict = {
        word[9]: {
            "original": word[8],
            "title": word[18],
            "authors": word[19],
            "context": word[5],
        } for word in kdb.get_dictionary()
    }
    kindle_words = kindle_dict.keys()
    log.debug("Kindle: %d records, like %s",
              len(kindle_words),
              kindle_words and kindle_dict[kindle_words[0]])
    kindle_words = set(kindle_words)

    auth = json.load(open("auth.json", "r"))
    ll = Lingualeo(**auth)
    ll.auth()
    lingualeo_dictionary = ll.get_dictionary()
    lingualeo_dict = {
        word["word_value"]:word for word in lingualeo_dictionary
    }

    lingualeo_words = lingualeo_dict.keys()
    log.debug("Lingualeo: %d records, like %s",
              len(lingualeo_words),
              lingualeo_words and lingualeo_dict[lingualeo_words[0]])
    lingualeo_words = set(lingualeo_words)

    lingualeo_learned_words = [
        word["word_value"] for word in lingualeo_dictionary
        if word['progress_percent'] == 100
    ]
    log.debug("Lingualeo: %d learned words, like %s",
              len(lingualeo_learned_words),
              lingualeo_learned_words and lingualeo_learned_words[0])
    lingualeo_learned_words = set(lingualeo_learned_words)

    new_words = kindle_words - lingualeo_words
    log.info("Found %d new words", len(new_words))

    learned_words = kindle_words & lingualeo_learned_words
    log.info("Need to update %d learned words", len(learned_words))

    for word in new_words:
        context = kindle_dict[word]["context"]

        original = kindle_dict[word]["original"]
        try:
            pos = context.index(original)
        except ValueError:
            pos = 0
        lw = pos - 30
        if lw < 0:
            lw = 0
        rw = pos + len(word) + 30
        if rw >= len(context):
            rw = len(context)
        log.debug("Context is %s", context[lw:rw])

        translations = ll.get_translation(word)
        if not translations:
            log.warn("No translations for %s, skip", word)
            continue

        if translations["is_exist"] != 0:
            log.warn("Exists %s, skip", word)
            continue

        log.debug("Translations for %s is %s",
                  word,
                  u", ".join(translations["twords"])[:60])

        translation = translations["twords"][0]
        ll.add_word(word, translation, context)

    for word in learned_words:
        log.debug("Set learn for %s", word)
        kdb.set_learn(word)

    kdb.conn.commit()

if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    sync("/media/kindle/system/vocabulary/vocab.db")
