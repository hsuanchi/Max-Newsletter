import json
import unittest
from unittest.mock import patch, call

from flask import url_for
from flask_testing import TestCase

from app import create_app, db
from app.views.celery_tasks.tasks import (
    send_check_mail,
    send_mail_task,
    send_mail_now_task,
    send_admin_mail_task,
)


class SettingBase(TestCase):
    def create_app(self):
        return create_app("testing")

    def tearDown(self):
        db.session.remove()


class Check_email(SettingBase):
    @patch("smtplib.SMTP")
    def test_send_check_mail(self, mock_smtp):
        send_check_mail("a0025071@gmail.com", lang="zh")
        self.assertTrue(mock_smtp.called)

    @patch("smtplib.SMTP")
    def test_send_weekly_mail(self, mock_smtp):
        send_mail_task()
        self.assertTrue(mock_smtp.called)

    @patch("smtplib.SMTP")
    def test_send_now_mail(self, mock_smtp):
        send_mail_now_task(email="a0025071@gmail.com")
        self.assertTrue(mock_smtp.called)

    @patch("smtplib.SMTP")
    def test_send_admin_mail(self, mock_smtp):
        send_admin_mail_task()
        self.assertTrue(mock_smtp.called)


if __name__ == "__main__":
    unittest.main()
