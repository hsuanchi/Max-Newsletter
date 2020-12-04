import unittest

from flask import url_for
from flask_testing import TestCase

from app import create_app, db


class SettingBase(TestCase):
    def create_app(self):
        return create_app("testing")

    def tearDown(self):
        db.session.remove()


class Check_api_article(SettingBase):
    def test_category_list_zh(self):
        response = self.client.get(
            url_for("index.get_article_category_list", lang_code="zh")
        )
        self.assertEqual(response.status_code, 200)
        self.assertGreater(len(response.data), 2)

    def test_article(self):
        response = self.client.get(url_for("index.article", lang_code="zh"))
        self.assertEqual(response.status_code, 200)
        self.assertGreater(len(response.data), 2)

    def test_article_zh(self):
        response = self.client.get(url_for("index.get_article", lang_code="zh"))
        self.assertEqual(response.status_code, 200)
        self.assertGreater(len(response.data), 2)

    def test_subscribes_number(self):
        response = self.client.get(
            url_for("index.get_subscribes_number", lang_code="zh")
        )
        self.assertEqual(response.status_code, 200)


if __name__ == "__main__":
    unittest.main()
