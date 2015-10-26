import os
import sys
sys.path.append(os.path.join(os.getcwd(), 'leagueChromeExtension_BackEnd'))
from fabric.api import local

def hello():
    print("Hello world!")


def cwd():
    import os
    print os.getcwd()


def runserver():
    from leagueChromeExtension import app
    app.run(debug=True)


def createdb():
    from leagueChromeExtension import db, app
    with app.app_context():
        db.create_all()


def updaterequirement():
    local("pip freeze > requirements.txt")




