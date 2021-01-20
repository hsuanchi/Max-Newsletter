from flask import (
    render_template,
    Blueprint,
    make_response,
)
from app import db
from app.model.article import Website_crawler_structure, Crawler_clean_data
import datetime

category = Blueprint("category", __name__)


@category.route("/<string:get_tid>/rss.xml")
def get_rss_by_tid(get_tid):

    day = (datetime.date.today() - datetime.timedelta(days=7)).strftime("%Y-%m-%d")

    crawler_data = (
        db.session.query(Website_crawler_structure)
        .join(Crawler_clean_data)
        .filter(Website_crawler_structure.tid == get_tid)
        .group_by(Crawler_clean_data.article_link)
        .filter(Crawler_clean_data.created_at > day)
        .with_entities(
            Website_crawler_structure.website_name,
            Website_crawler_structure.tid,
            Crawler_clean_data,
        )
        .all()
    )

    template = render_template("rss.xml", data=crawler_data)
    response = make_response(template)
    response.headers["Content-Type"] = "application/xml"
    return response
