# -*- coding: utf-8 -*-
# https://raw.githubusercontent.com/relaxart/LeoPort/a2592025284d5d179168e096e4aa1fc259c6b905/service.py

import urllib
import urllib2
import json
from cookielib import CookieJar


class Lingualeo:

    API_URL = "https://api.lingualeo.com"
    WEB_URL = "https://lingualeo.com"

    def __init__(self, email, password):
        self.email = email
        self.password = password
        self.cj = CookieJar()

    def _get(self, url, values=None):
        data = values and urllib.urlencode(values)

        opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(self.cj))
        req = opener.open(url, data)

        return json.loads(req.read())

    def auth(self):
        url = Lingualeo.API_URL + "/api/login"
        values = {
            "email": self.email,
            "password": self.password
        }

        return self._get(url, values)

    def add_word(self, word, tword, context=None):
        url = Lingualeo.API_URL + "/addword"
        values = {
            "word": word.encode('utf-8'),
            "tword": tword.encode('utf-8'),
        }
        if context:
            values["context"] = context.encode('utf-8')
        return self._get(url, values)

    def get_dictionary(self):
        url = Lingualeo.WEB_URL + "/userdict/json?"
        values = {
            "page": 1,
        }
        dictionary = []
        while True:
            response = self._get(url + urllib.urlencode(values))

            for dicts in response["userdict3"]:
                dictionary.extend(dicts["words"])

            if not response["show_more"]:
                return dictionary

            values["page"] += 1

    def get_translation(self, word):
        url =  "{}/gettranslates?word={}".format(
            Lingualeo.API_URL,
            urllib.quote_plus(word.encode('utf-8'))
        )

        result = self._get(url)
        twords = [word['value'] for word in result.get("translate", [])]
        return twords and {
            "is_exist": result["is_user"],
            "twords": twords
        }