from ...model.article import Crawler_clean_data, Website_crawler_structure


def clean_crawler_data():

    querys = Crawler_clean_data.get_raw_crawler_data()
    tasks = translate_and_save_data(querys)
    print(tasks)
    return tasks


def translate_and_save_data(website_db):

    # Import Google Translate 相關
    from google.cloud import translate_v2 as translate

    translate_client = translate.Client()

    for i in range(len(website_db)):

        web_structure = Website_crawler_structure.query.filter_by(
            id=int(website_db.loc[i, "tid"])
        ).first()

        crawler_description = website_db["crawler_description"][i]
        crawler_name = website_db["crawler_name"][i]
        crawler_lang = website_db["translate"][i]

        if crawler_lang == 1:

            description_zh = translate_client.translate(
                crawler_description, source_language="en", target_language="zh-TW"
            )["translatedText"]

            name_zh = translate_client.translate(
                crawler_name, source_language="en", target_language="zh-TW"
            )["translatedText"]

            description_en = crawler_description
            name_en = crawler_name

        elif crawler_lang == 0:

            description_en = translate_client.translate(
                crawler_description, source_language="zh-TW", target_language="en"
            )["translatedText"]

            name_en = translate_client.translate(
                crawler_name, source_language="zh-TW", target_language="en"
            )["translatedText"]

            description_zh = crawler_description
            name_zh = crawler_name

        clean_data = Crawler_clean_data(
            article_name_en=name_en,
            article_name_ch=name_zh,
            article_description_en=description_en,
            article_description_ch=description_zh,
            article_link=website_db.loc[i, "crawler_link"],
            tid=web_structure.id,
        )
        clean_data.save()
    return len(website_db)
