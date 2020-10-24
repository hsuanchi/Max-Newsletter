from flask import Flask, g, render_template, jsonify, request, session, redirect, url_for, Blueprint, make_response
from sqlalchemy.orm import joinedload
from sqlalchemy.orm import contains_eager

import datetime
from .. import db, cache
from ..model.article import Website_crawler_structure, Website_tag, Website_tag_schema, Article_tag_schema, Crawler_clean_data
from ..model.email import EmailModel

index = Blueprint('index', __name__)
website_tag_schema = Website_tag_schema()
article_tag_schema = Article_tag_schema()


@index.route('/')
def article():
    return render_template('index.html')


@index.route('/api/get_article_category_list')
@cache.cached(timeout=60 * 60 * 12)
def get_article_category_list():
    querys = db.session.query(Website_tag)\
        .options(joinedload(Website_tag.wid))\
        .order_by(Website_tag.sequence)\
        .all()

    serialize = website_tag_schema.dump(querys, many=True)
    return jsonify(serialize), 200


@index.route('/api/get_article')
@cache.cached(timeout=60 * 60 * 12)
def get_article():
    day = (datetime.date.today() -
           datetime.timedelta(days=7)).strftime("%Y-%m-%d")

    querys = db.session.query(Website_tag)\
            .outerjoin(Website_crawler_structure)\
            .join(Crawler_clean_data)\
            .options(contains_eager(Website_tag.wid)\
            .contains_eager(Website_crawler_structure.crawler_data))\
            .filter(Crawler_clean_data.created_at > day)\
            .group_by(Crawler_clean_data.article_link)\
            .order_by(Website_tag.sequence,Crawler_clean_data.created_at.desc())\
            .all()

    serialize = article_tag_schema.dump(querys, many=True)
    return jsonify(serialize), 200


@index.route('/api/get_subscribes_number')
@cache.cached(timeout=60 * 3)
def get_subscribes_number():
    querys = db.session.query(EmailModel).count()
    return str(querys + 100), 200
