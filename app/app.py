from flask import Flask, redirect, url_for
import os
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager, logout_user
from flask_bootstrap import Bootstrap


app = Flask(__name__)
FLASK_ENV = os.environ.get("FLASK_ENV") or 'development'
app.config.from_object('app.config.%s%sConfig' % (FLASK_ENV[0].upper(), FLASK_ENV[1:]))


bootstrap = Bootstrap(app)

db = SQLAlchemy(app)
migrate = Migrate(app, db)
login = LoginManager(app)


# from models import Product, Sale, Warehouse, Supplier
db.create_all()


# region Views
@app.route('/')
def index():
    return ' '


@app.route('/register', methods=['GET', 'POST'])
def register():
    return ' '


@app.route('/login', methods=['GET', 'POST'])
def login():
    return ' '


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


# endregion




