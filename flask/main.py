import os
from dotenv import load_dotenv

# load .env
dotenv_path = os.path.join(os.path.dirname(__file__), '.flaskenv')
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path, override=True)

from app import create_app, db
from flask_migrate import Migrate, upgrade, migrate

app = create_app(os.environ.get('FLASK_ENV'))

migrates = Migrate(app=app, db=db)


@app.shell_context_processor
def make_shell_context():
    return dict(app=app, db=db)


@app.cli.command()
def deploy():
    upgrade()


@app.cli.command()
def test():
    import unittest
    import sys

    tests = unittest.TestLoader().discover("tests")
    result = unittest.TextTestRunner(verbosity=2).run(tests)
    if result.errors or result.failures:
        sys.exit(1)
