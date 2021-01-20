from app import db
from datetime import datetime
from marshmallow import Schema, fields


class EmailModel(db.Model):
    __tablename__ = "email_subscribe"
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(55))
    insert_time = db.Column(db.DateTime, default=datetime.now)
    status = db.Column(db.Boolean)

    @classmethod
    def get_by_email(cls, email):
        filters = {"email": email, "status": True}
        return cls.query.filter_by(**filters).first()

    @classmethod
    def subscribe(cls, email):
        filters = {"email": email}
        check_exit_email = cls.query.filter_by(**filters).first()
        if check_exit_email:
            check_exit_email.status = True
            db.session.commit()
        else:
            create_subscribe = cls(email=email, status=True)
            db.session.add(create_subscribe)
            db.session.commit()

    @classmethod
    def unsubscribe(cls, email):
        filters = {"email": email}
        get_exit_email = cls.query.filter_by(**filters).first()
        get_exit_email.status = False
        db.session.commit()


class Email_subscribe_log(db.Model):
    __tablename__ = "email_subscribe_log"
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(55))
    insert_time = db.Column(db.DateTime, default=datetime.now)

    @classmethod
    def subscribe(cls, email):
        create_subscribe = cls(email=email)
        db.session.add(create_subscribe)
        db.session.commit()


class Email_unsubscribe_log(db.Model):
    __tablename__ = "email_unsubscribe_log"
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(55))
    insert_time = db.Column(db.DateTime, default=datetime.now)

    @classmethod
    def unsubscribe(cls, email):
        create_subscribe = cls(email=email)
        db.session.add(create_subscribe)
        db.session.commit()


class EmailSchema(Schema):
    email = fields.Email()
