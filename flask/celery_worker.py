import os
from dotenv import load_dotenv
from app import create_app, celery

# load .env
dotenv_path = os.path.join(os.path.dirname(__file__), ".flaskenv")
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path, override=True)

app = create_app(os.environ.get("FLASK_ENV"))
app.app_context().push()
