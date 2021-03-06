"""empty message

Revision ID: 2e1cbe11b910
Revises: 
Create Date: 2020-11-17 17:43:09.461458

"""
from alembic import op
import sqlalchemy as sa
from datetime import date

# revision identifiers, used by Alembic.
revision = "0001_generated"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    insert_email = op.create_table(
        "email_subscribe",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("email", sa.String(length=55), nullable=True),
        sa.Column("insert_time", sa.DateTime(), nullable=True),
        sa.Column("status", sa.Boolean(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "email_subscribe_log",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("email", sa.String(length=55), nullable=True),
        sa.Column("insert_time", sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "email_unsubscribe_log",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("email", sa.String(length=55), nullable=True),
        sa.Column("insert_time", sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
    insert_website_tag = op.create_table(
        "website_tag",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=True),
        sa.Column("updated_at", sa.DateTime(), nullable=True),
        sa.Column("tag", sa.String(length=50), nullable=True),
        sa.Column("sequence", sa.Integer(), nullable=True),
        sa.Column("line_bot_url", sa.String(length=255), nullable=True),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("tag"),
    )
    insert_website_structure = op.create_table(
        "website_crawler_structure",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=True),
        sa.Column("updated_at", sa.DateTime(), nullable=True),
        sa.Column("website_name", sa.String(length=255), nullable=True),
        sa.Column("website_url", sa.String(length=255), nullable=True),
        sa.Column("crawler_url", sa.String(length=255), nullable=True),
        sa.Column("crawler_type", sa.String(length=55), nullable=True),
        sa.Column("css_name", sa.String(length=255), nullable=True),
        sa.Column("css_description", sa.String(length=255), nullable=True),
        sa.Column("css_link", sa.String(length=255), nullable=True),
        sa.Column("status", sa.String(length=255), nullable=True),
        sa.Column("translate", sa.Integer(), nullable=True),
        sa.Column("tid", sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(
            ["tid"],
            ["website_tag.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    insert_crawler_data = op.create_table(
        "crawler_clean_data",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=True),
        sa.Column("updated_at", sa.DateTime(), nullable=True),
        sa.Column("article_name_en", sa.Text(), nullable=True),
        sa.Column("article_name_ch", sa.Text(), nullable=True),
        sa.Column("article_description_en", sa.Text(), nullable=True),
        sa.Column("article_description_ch", sa.Text(), nullable=True),
        sa.Column("article_link", sa.Text(), nullable=True),
        sa.Column("tid", sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(
            ["tid"],
            ["website_crawler_structure.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    # ### end Alembic commands ###

    op.bulk_insert(
        insert_email,
        [{"email": "a0025071@gmail.com", "status": 1, "insert_time": date.today()}],
    )
    op.bulk_insert(
        insert_website_structure,
        [
            {
                "created_at": date.today(),
                "updated_at": date.today(),
                "website_name": "web.dev",
                "website_url": "https://developers.google.com/web/updates",
                "status": "Y",
                "translate": 1,
                "tid": 1,
            }
        ],
    )
    op.bulk_insert(
        insert_website_tag,
        [
            {
                "created_at": date.today(),
                "updated_at": date.today(),
                "tag": "Google Product updates",
                "sequence": 1,
            }
        ],
    )
    op.bulk_insert(
        insert_crawler_data,
        [
            {
                "created_at": date.today(),
                "updated_at": date.today(),
                "article_name_en": "What's New In DevTools (Chrome 88)",
                "article_name_ch": "DevTools（Chrome 88）的新增功能",
                "article_description_en": "What's New In DevTools (Chrome 88) Faster DevTools startup DevTools startup now is ~37% faster in terms of JavaScript compilation (from 6.9s down to 5s)! 🎉 The team did some optimization to reduce the performance overhead of serialisation, parsing and deserialisation during the startup.",
                "article_description_ch": "DevTools（Chrome 88）中的新增功能更快的DevTools啟動在JavaScript編譯方面，DevTools啟動現在快了37％（從6.9s降至5s）！ 🎉團隊進行了一些優化，以減少啟動過程中序列化，解析和反序列化的性能開銷。即將發布的工程博客文章將詳細介紹該實現。敬請關注！ Chromium問題：1029427新的CSS角度可視化工具DevTools現在對CSS有更好的支持",
                "article_link": "https://developers.google.com/web/updates/2020/11/devtools",
                "tid": 1,
            }
        ],
    )


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("crawler_clean_data")
    op.drop_table("website_crawler_structure")
    op.drop_table("website_tag")
    op.drop_table("email_unsubscribe_log")
    op.drop_table("email_subscribe_log")
    op.drop_table("email_subscribe")
    # ### end Alembic commands ###
