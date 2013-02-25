#-*- coding:utf-8 -*-

import os
from unittest import TestCase

from jblog import conf

ME_LOC = os.path.dirname(os.path.abspath(__file__))


class ConfParserTestCase(TestCase):

    def _get_file(self, filenames):

        return [os.path.join(ME_LOC, filename) for filename in filenames]

    def test_success(self):
        cfg= conf.Config(self._get_file(['default.ini']))
        self.assertEqual(cfg.db_name, 'mysql')
        self.assertEqual(cfg.multi_value, 'v1\nv2\nv3\nv4')
        self.assertEqual(cfg.mysql_host, '192.168.0.90')
        self.assertEqual(len(cfg), 3)
        self.assertEqual(cfg.get('db_name', 'DEFAULT'), 'mysql')

    def test_overwrite(self):
        cfg = conf.Config(self._get_file(['default.ini', 'live.ini']))
        self.assertEqual(cfg.db_name, 'sqlite3')
        self.assertEqual(cfg.multi_value, 'v1\nv2\nv3\nv4')
        self.assertEqual(cfg.mysql_host, '192.168.0.90')
        self.assertEqual(len(cfg), 4)
        self.assertEqual(cfg.get('db_name', 'DEFAULT'), 'sqlite3')

