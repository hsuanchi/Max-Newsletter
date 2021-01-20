import datetime
from app import db, cache
from app.model.article import (
    Website_crawler_structure,
    Website_tag,
    Crawler_clean_data,
)
from sqlalchemy.orm import contains_eager

from flask import current_app, render_template
from flask_jwt_extended import create_access_token

# SMTP
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


def send_mail(
    send_subject: str,
    send_from: str,
    send_to: list,
    send_html_path: str,
    send_type: str,
    *args,
    **kwargs,
):

    with smtplib.SMTP(host="smtp.gmail.com", port="587") as smtp:  # 設定SMTP伺服器
        try:
            smtp.ehlo()  # 驗證 SMTP 伺服器
            smtp.starttls()  # 建立加密傳輸
            smtp.login(
                os.environ.get("email_username"), os.environ.get("email_password")
            )

            for user in send_to:
                text = ""

                # Send Weekly Email
                if send_type == "multiple":
                    content = MIMEMultipart()
                    content["Subject"] = send_subject
                    content["From"] = send_from
                    content["To"] = user
                    html = send_schedule_mail(
                        send_html_path, user=user, *args, **kwargs
                    )
                # Send Validate Email
                else:
                    content = MIMEMultipart()
                    content["Subject"] = send_subject
                    content["From"] = send_from
                    content["To"] = user
                    html = render_template(send_html_path, user=user, *args, **kwargs)

                content.attach(MIMEText(html, "html"))
                content.attach(MIMEText(text, "plain"))

                smtp.send_message(content)  # 寄送郵件

                print(user + "成功傳送")

        except Exception as e:
            print("Error in sending emails: ", e)


def send_schedule_mail(send_html_path, user, *args, **kwargs):
    jwt_token = create_access_token(identity=user)
    unsubscribe_email_path = (
        current_app.config["HOST_NAME"] + f"/en/email/unsubscribe?jwt_token={jwt_token}"
    )
    crawler = get_email_html()
    html = render_template(
        send_html_path,
        crawler_data=crawler,
        user=user,
        unsubscribe_email_path=unsubscribe_email_path,
        *args,
        **kwargs,
    )
    print(len(html))
    return html


@cache.cached(timeout=60 * 60 * 12, key_prefix="get_email")
def get_email_html():

    day = (datetime.date.today() - datetime.timedelta(days=7)).strftime("%Y-%m-%d")

    querys = (
        db.session.query(Website_tag)
        .outerjoin(Website_crawler_structure)
        .join(Crawler_clean_data)
        .options(
            contains_eager(Website_tag.wid).contains_eager(
                Website_crawler_structure.crawler_data
            )
        )
        .filter(Crawler_clean_data.created_at > day)
        .group_by(Crawler_clean_data.article_link)
        .order_by(Website_tag.sequence, Crawler_clean_data.created_at.desc())
        .all()
    )
    return querys
