# This file is placed in the Public Domain.


import json
import os
import unittest


from gcid.objects import Object
from gcid.storage import Db, Wd, save


import gcid.storage


Wd.workdir = ".test"


ATTRS1 = (
         'Classes',
         'Db',
         'Wd',
         'last',
         'save'
        )


ATTRS2 = (
          '__class__',
          '__delattr__',
          '__dict__',
          '__dir__',
          '__doc__',
          '__eq__',
          '__format__',
          '__ge__',
          '__getattribute__',
          '__gt__',
          '__hash__',
          '__init__',
          '__init_subclass__',
          '__le__',
          '__lt__',
          '__module__',
          '__ne__',
          '__new__',
          '__reduce__',
          '__reduce_ex__',
          '__repr__',
          '__setattr__',
          '__sizeof__',
          '__str__',
          '__subclasshook__',
          '__weakref__',
          'all',
          'find',
          'fns',
          'hook',
          'last',
          'match'
         )


class TestStorage(unittest.TestCase):

    def test_constructor(self):
        obj = Db()
        self.assertTrue(type(obj), Db)

    def test__class(self):
        obj = Db()
        clz = obj.__class__()
        self.assertTrue("Db" in str(type(clz)))

    def test_dirmodule(self):
        self.assertEqual(
                         dir(gcid.storage),
                         list(ATTRS1)
                        )

    def test_dirobject(self):
        db = Db()
        self.assertEqual(
                         dir(db),
                         list(ATTRS2)
                        )

    def test_module(self):
        self.assertTrue(Db().__module__, "gcid.storage")

    def test_save(self):
        Wd.workdir = ".test"
        obj = Object()
        path = save(obj)
        self.assertTrue(os.path.exists(os.path.join(Wd.workdir, "store", path)))
