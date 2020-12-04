from flask import current_app
from flask_jwt_extended import create_access_token

from ... import db, celery
from .send_email import send_mail
from .crawler import main
from .clean_table import clean_crawler_data
from celery.exceptions import Retry

import random


# Daily - Crawler data
@celery.task(name="crawler_all_everyday")
def crawler_all_everyday():
    obj_Crawler = main.Crawler()
    return obj_Crawler.crawl(db, "All")


# Daily - Crawler Clean data
@celery.task(bind=True, name="clean_data_everyday")
def clean_data_everyday(self):
    try:
        return clean_crawler_data()
    except Exception as e:
        self.retry(countdown=5, exc=e, max_retries=2)


# Send Submit Mail
@celery.task(name="send_check_mail")
def send_check_mail(email, lang="zh"):
    send_subject = "🚀 訂閱確認信"
    send_from = "Max 行銷誌"
    send_to = [email]
    send_html_path = f"/email/submit_mail_{lang}.html"
    jwt_token = create_access_token(identity=email)

    check_email_path = (
        current_app.config["HOST_NAME"]
        + f"/{lang}/email/subscribe?jwt_token={jwt_token}"
    )

    send_mail(
        send_subject,
        send_from,
        send_to,
        send_html_path,
        send_type="only_one_user",
        check_email_path=check_email_path,
    )
    return "66"


# Send Weekly Mail
@celery.task(name="send_week_mail_task")
def send_mail_task():
    send_subject = "🚀 每週四 - 掌握行銷大小事"
    send_from = "Max 行銷誌"

    sql_subscribe_email = """
        SELECT
            email
        FROM
            email_subscribe
        WHERE
            status = TRUE
    """

    subscribe_email = db.engine.execute(sql_subscribe_email)
    send_to = [email[0] for email in subscribe_email]
    send_html_path = "/email/mail_template.html"
    return send_mail(
        send_subject, send_from, send_to, send_html_path, send_type="multiple"
    )


# Send Test Mail
@celery.task(name="send_now_mail_task")
def send_mail_now_task(email="a0025071@gmail.com"):

    send_subject = "每週四 - 掌握行銷大小事 (Test)"
    send_from = "Max 行銷誌"
    send_to = [email]

    send_html_path = "/email/mail_template.html"
    send_mail(send_subject, send_from, send_to, send_html_path, send_type="multiple")

    return "666"


# Send Daily Mail
@celery.task(name="send_admin_mail_task")
def send_admin_mail_task():
    send_subject = "🚀 每週四 - 掌握行銷大小事 (Daily)"
    send_from = "Max 行銷誌"
    send_to = ["max@turingdigital.com.tw", "a0025071@gmail.com"]
    send_html_path = "/email/mail_template.html"
    return send_mail(
        send_subject, send_from, send_to, send_html_path, send_type="multiple"
    )
