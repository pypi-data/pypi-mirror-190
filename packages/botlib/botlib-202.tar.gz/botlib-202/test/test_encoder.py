# This file is placed in the Public Domain.


import json
import os
import unittest


from bot.objects import Object, oid
from bot.encoder import ObjectDecoder, ObjectEncoder, dump, dumps
from bot.encoder import load, loads
from bot.storage import Wd


VALIDJSON = '{"test": "bla"}'


class TestEncoder(unittest.TestCase):

    def test_json(self):
        obj = Object()
        obj.test = "bla"
        oobj = loads(dumps(obj))
        self.assertEqual(oobj.test, "bla")

    def test_jsondump(self):
        obj = Object()
        obj.test = "bla"
        self.assertEqual(dumps(obj), VALIDJSON)

    def test_load(self):
        obj = Object()
        obj.key = "value"
        pld = dump(obj, Wd.getpath(oid(obj)))
        oobj = Object()
        load(oobj, pld)
        self.assertEqual(oobj.key, "value")
