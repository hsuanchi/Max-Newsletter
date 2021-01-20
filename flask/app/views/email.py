from flask import (
    render_template,
    request,
    Blueprint,
    g,
    current_app,
)
from marshmallow import ValidationError, EXCLUDE
from flask_jwt_extended import (
    get_jwt_identity,
    jwt_required,
    jwt_optional,
)
from app.model.email import (
    EmailModel,
    EmailSchema,
    Email_subscribe_log,
    Email_unsubscribe_log,
)
from app.model.article import (
    Article_tag_schema,
)
from app.views.abort_msg import abort_msg
from app.views.celery_tasks.tasks import send_mail_now_task, send_check_mail

email = Blueprint("email", __name__)
email_schema = EmailSchema()
article_tag_schema = Article_tag_schema()


# Subscribe Email
@email.route("/subscribe", methods=["GET", "POST"])
@jwt_optional
def subscribe():
    # Submit Result Page
    if request.method == "GET":
        # Validate
        data = get_jwt_identity()
        if data:
            EmailModel.subscribe(data)
            Email_subscribe_log.subscribe(data)
            return render_template(
                "/email/submit_result_success.html", result_type="Register success"
            )

    # Send Submit Mail work
    if request.method == "POST":
        try:
            # Validate
            data = request.json
            data_valide = email_schema.load(data, unknown=EXCLUDE)
            # Check Mail exist or not
            if EmailModel.get_by_email(data_valide["email"]):
                return {"message": "already"}, 200
            else:
                lang = g.get("lang_code")
                send_check_mail.delay(data_valide["email"], lang)
                return {"message": "send"}, 200

        except ValidationError as error:
            current_app.logger.error(error.messages)
            return {"errors": error.messages}, 400

        except Exception as e:
            current_app.logger.error(abort_msg(e))
            return {"errors": abort_msg(e)}, 422


# Unsubscribe Email
@email.route("/unsubscribe", methods=["GET"])
@jwt_required
def unsubscribe():
    data = get_jwt_identity()
    if data:
        EmailModel.unsubscribe(data)
        Email_unsubscribe_log.unsubscribe(data)
        return render_template(
            "/email/submit_result_success.html", result_type="Unsubscribe success"
        )


# Testing Email
@email.route("/")
def test():
    data = request.values
    if data:
        send_mail_now_task.delay(data["email"])
    else:
        send_mail_now_task.delay()
    return "666"
