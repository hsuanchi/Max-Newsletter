import json
import unittest
from unittest.mock import patch, call

from flask import url_for
from flask_testing import TestCase

from app import create_app, db


class SettingBase(TestCase):
    def create_app(self):
        return create_app("testing")

    def tearDown(self):
        db.session.remove()


class Check_rss(SettingBase):
    def test_rss(self):
        response = self.client.get(
            url_for('category.get_rss_by_tid', get_tid='1', lang_code='zh'))

        self.assertEqual(response.status_code, 200)
        self.assertGreater(len(response.data), 2)


if __name__ == '__main__':
    unittest.main()