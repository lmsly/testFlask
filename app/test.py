from flask import Flask
app = Flask(__name__)
import config
from exts import db
app.config.from_object(config)
db.init_app(app)

from app import views