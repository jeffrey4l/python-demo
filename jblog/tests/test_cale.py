#-*- coding:utf-8 -*-

import unittest

from jblog.utils import cacl

class AddIntTest(unittest.TestCase):

    def test_add(self):
        self.assertEqual(5, cacl.add_int(3, 2))
        


