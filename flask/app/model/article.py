from .. import db
from .mixin.basic import BasicModelMixin

from datetime import datetime
import pandas as pd
from marshmallow import Schema, fields


class Website_crawler_structure(db.Model, BasicModelMixin):
    __tablename__ = "website_crawler_structure"
    website_name = db.Column(db.String(255))
    website_url = db.Column(db.String(255))
    crawler_url = db.Column(db.String(255))
    crawler_type = db.Column(db.String(55))
    css_name = db.Column(db.String(255))
    css_description = db.Column(db.String(255))
    css_link = db.Column(db.String(255))
    status = db.Column(db.String(255))
    translate = db.Column(db.Integer)

    # 多
    tid = db.Column(db.Integer, db.ForeignKey("website_tag.id"))
    # 一
    crawler_data = db.relationship(
        "Crawler_clean_data",
        lazy="select",
        backref=db.backref("crawler_data", lazy="select"),
    )


class Website_tag(db.Model, BasicModelMixin):
    __tablename__ = "website_tag"
    tag = db.Column(db.String(50), unique=True)
    sequence = db.Column(db.Integer)
    line_bot_url = db.Column(db.String(255))

    # 一
    wid = db.relationship(
        "Website_crawler_structure",
        lazy="select",
        backref=db.backref("website", lazy="select"),
    )


class Crawler_clean_data(db.Model, BasicModelMixin):
    __tablename__ = "crawler_clean_data"
    article_name_en = db.Column(db.Text())
    article_name_ch = db.Column(db.Text())
    article_description_en = db.Column(db.Text())
    article_description_ch = db.Column(db.Text())
    article_link = db.Column(db.Text())

    # 多
    tid = db.Column(db.Integer, db.ForeignKey("website_crawler_structure.id"))

    @staticmethod
    def get_raw_crawler_data():
        sql_article = """
            SELECT
                *
            FROM (
                SELECT
                    wid AS tid,
                    crawler_name,
                    crawler_description,
                    crawler_link,
                    insert_time AS created_at,
                    translate,
                    TIMESTAMPDIFF(DAY, ANY_VALUE(insert_time), now()) AS count_time
                FROM
                    crawlerData
                LEFT JOIN website_crawler_structure ON crawlerData.wid = website_crawler_structure.id
            GROUP BY
                crawler_name
            ORDER BY
                insert_time DESC
            LIMIT 50) AS A
            WHERE
                A.count_time = 0
            ORDER BY
                count_time
            """

        return pd.read_sql(sql_article, db.engine)


# Article Category List Schema
class Website_crawler_schema(Schema):
    website_name = fields.String(dump_only=True)
    website_url = fields.String(dump_only=True)
    status = fields.String(dump_only=True)


class Website_tag_schema(Schema):
    sequence = fields.Integer(dump_only=True)
    tag = fields.String()
    wid = fields.List(fields.Nested(Website_crawler_schema))


# Article List Schema
class Crawler_clean_data_schema(Schema):
    article_name_en = fields.String()
    article_name_ch = fields.String()
    article_description_en = fields.String()
    article_description_ch = fields.String()
    article_link = fields.String()
    created_at = fields.DateTime(format="%Y-%m-%d")


class Article_crawler_schema(Schema):
    website_name = fields.String(dump_only=True)
    status = fields.String(dump_only=True)
    crawler_data = fields.List(fields.Nested(Crawler_clean_data_schema))


class Article_tag_schema(Schema):
    sequence = fields.Integer(dump_only=True)
    tag = fields.String()
    wid = fields.List(fields.Nested(Article_crawler_schema))
