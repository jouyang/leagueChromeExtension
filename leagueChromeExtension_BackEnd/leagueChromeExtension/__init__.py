from flask.ext.api import FlaskAPI
from leagueChromeExtension.configModule import DevelopmentConfig
from flask.ext.sqlalchemy import SQLAlchemy

db = SQLAlchemy()

app = FlaskAPI(__name__)
app.config.from_object('leagueChromeExtension.configModule.DevelopmentConfig')
db.init_app(app)

import leagueChromeExtension.views
