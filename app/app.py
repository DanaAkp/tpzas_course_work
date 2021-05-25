from flask import Flask, redirect, url_for, render_template, flash, request
import os

from flask_admin.menu import MenuLink
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager, logout_user, current_user, login_user
from flask_bootstrap import Bootstrap
from flask_admin import Admin, AdminIndexView, expose
from app.forms import RegisterForm, LoginForm
from AES.aes import AES


app = Flask(__name__)
FLASK_ENV = os.environ.get("FLASK_ENV") or 'development'
app.config.from_object('app.config.%s%sConfig' % (FLASK_ENV[0].upper(), FLASK_ENV[1:]))


bootstrap = Bootstrap(app)

db = SQLAlchemy(app)
migrate = Migrate(app, db)
login = LoginManager(app)
key = b'1234567890123456'
aes = AES(key)


from app.models import Product, Sale, Warehouse, Supplier, User, Role, Unit, Category


@login.user_loader
def load_user(id):
    return User.query.get(int(id))


class DashboardView(AdminIndexView):

    def is_visible(self):
        return False


admin = Admin(app, name='Database', template_mode='bootstrap3', index_view=DashboardView())


from app.admin import WarehouseModel, ModelForAdmin, SaleModel, PurchasingDepartment
db.create_all()

admin.add_views(ModelForAdmin(User, db.session))
admin.add_views(ModelForAdmin(Role, db.session))

admin.add_views((WarehouseModel(Product, db.session)))
admin.add_views((SaleModel(Sale, db.session)))
admin.add_views((WarehouseModel(Warehouse, db.session)))
admin.add_views((WarehouseModel(Supplier, db.session)))
admin.add_views((WarehouseModel(Unit, db.session)))
admin.add_views((WarehouseModel(Category, db.session)))
with app.test_request_context():
    admin.add_link(MenuLink(name='Home', category='', url='/'))


# region Views
@app.route('/')
def index():
    # TODO add register
    return render_template('index.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if request.method == 'POST':
        user_name = form.username.data
        password = form.password.data
        if User.query.filter_by(name=user_name).first() is None:
            new_user = User()
            new_user.name=user_name
            new_user.role_id=2
            new_user.set_password(password)
            db.session.add(new_user)
            db.session.commit()
        else:
            flash('User name is exist!')
            return render_template('register.html', form=form)
    return render_template('register.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if current_user.is_authenticated:
        return render_template('index.html')
    if form.validate_on_submit():
        user = User.query.filter_by(name=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password!')
            return render_template('login.html', form=form)
        login_user(user)
        return redirect(url_for('index'))
    return render_template('login.html', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


# endregion




