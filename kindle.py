# -*- coding: utf-8 -*-

import sqlite3

class KindleV5:

    def __init__(self, dbfile):
        self.conn = sqlite3.connect(dbfile)
        self.conn.text_factory = lambda x: unicode(x, "utf-8", "ignore")

    def get_dictionary(self):
        """
        :return: list of joined lookups
        """
        cur = self.conn.cursor()

        cur.execute("SELECT * "
                    "FROM lookups "
                    "INNER JOIN words ON words.id=lookups.word_key "
                    "INNER JOIN book_info ON book_info.id=lookups.book_key "
                    "WHERE words.lang='en' AND words.category=0")

        return cur.fetchall()

    def set_learn(self, word):
        cur = self.conn.cursor()
        cur.execute("UPDATE words SET category=100 WHERE stem=?",
                    (word.encode("utf-8"),) )