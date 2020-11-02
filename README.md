# [Max 行銷誌電子報](https://article.maxlist.xyz/)

### 1. Side Project 原由：

很喜歡的一句話是：「我們都是環境下的產物」，說明其實看似每個決定都是自己在做選擇，但其實促成每個決定的背後都是過去所獲得的資訊累積。\
這專案希望能讓自己更留意平時被餵食的資訊，所以精選了 21 個平常會關注的網站，用爬蟲追蹤資訊並整理電子報。

於每週四下午四點，一封電子報，帶大家掌握行銷大小事 - [Max 行銷誌電子報](https://article.maxlist.xyz/)


### 2. 使用技術：

Background Tasks:
* Celery
* Flower
* Redis

Flask Extension:
* Flask-JWT-Extended
* Flask-SQLAlchemy
* Flask-Migrate
* Flask-Caching
* Flask-Babel

Crawler:
* Beautifulsoup
* Feedparser
* Cloudscraper

Mail Server:
* Smtplib

Web Server:
* Nginx
* uWSGI

Testing:
* Unittest
* Mock
* Coverage

FrontEnd:
* Bootstrap 4
* jQuery

### 3. 貢獻
PRs are welcome!

#### Setup Development Environment
##### Prerequisite Setup
###### Customize Your Own Flask Environment

You may create your own `flask/.flaskenv` to customize your own flask environment for development. For example, see `flaskenv.sample`:

```
export FLASK_APP=main.py

export FLASK_ENV=development

export JWT_SECRET_KEY='THIS JWT Key made by max super secert'
export SECRET_KEY='THIS IS MAX set to be super secert'

export db='sqlite:////tmp/test.db'
export email_password='your email server password'
export email_username='your email username'
export GOOGLE_APPLICATION_CREDENTIALS='the gcp credentials'
```

Copy an edited `flaskenv.sample` to `flask/.flaskenv`.


###### Create SSL Key and Certificate for NGINX

If your development environment also manipulates a container of nginx server, you need the SSL key and certificate. Create them by the following commands:

```
$ cd ./nginx.conf
$ openssl req -x509 -nodes -days 3650 -newkey rsa:2048 -keyout ssl.key -out ssl.csr
```


##### Launch Docker Container

Now you are ready to build a development environment quickly by the following commands:

```
$ docker-compose pull
$ docker-compose -f ./docker-compose.yml up --build -d
```

Clean the docker containers after completing development

```
docker-compose stop ; docker-compose rm -f
```


##### Dive Into the Code

The entry point of the whole flask application is `main.py` when launching and `index.py` for url root. No matter which development tool or IDE is, you may want to put your breakpoint here. Remember to refresh the browser page to trigger the process to get into `index.py`.