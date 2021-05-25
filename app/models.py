from flask_login import UserMixin
from sqlalchemy.orm import reconstructor

from app.app import db, aes
from werkzeug.security import generate_password_hash, check_password_hash


class Product(db.Model):
    __tablename__ = 'products'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    shelf_life = db.Column(db.Date, nullable=False)
    trade_price = db.Column(db.Integer, nullable=False)

    id_unit = db.Column(db.Integer, db.ForeignKey('units.id'), nullable=False)
    id_category = db.Column(db.Integer, db.ForeignKey('categories.id'), nullable=False)
    id_supplier = db.Column(db.Integer, db.ForeignKey('suppliers.id'), nullable=False)

    sale = db.relationship('Sale', backref='products')
    warehouse = db.relationship('Warehouse', backref='products')

    def __str__(self):
        return self.name


class Unit(db.Model):
    __tablename__ = 'units'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    abbreviation = db.Column(db.String(10))
    product = db.relationship('Product', backref='units')

    def __str__(self):
        return self.name


class Category(db.Model):
    __tablename__ = 'categories'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    product = db.relationship('Product', backref='categories')
    supplier = db.relationship('Supplier', backref='categories')

    def __str__(self):
        return self.name


class Supplier(db.Model):
    __tablename__ = 'suppliers'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    address = db.Column(db.Text, nullable=False)
    contacts = db.Column(db.Integer, nullable=False)
    contract_number = db.Column(db.Integer)
    id_category = db.Column(db.Integer, db.ForeignKey('categories.id'), nullable=False)
    product = db.relationship('Product', backref='suppliers')

    def __init__(self, id, name, address, contacts, contract_number, id_category):
        self.id = id
        self.name = self.encrypt(name)
        self.address = self.encrypt(address)
        self.contacts = self.encrypt(contacts)
        self.contract_number = self.encrypt(contract_number)
        self.id_category = id_category

        self.init_on_load()

    @reconstructor
    def init_on_load(self):
        pass

    def encrypt(self, value):
        key = b'1234567890123456'
        value = bytes(str(value))
        return aes.encrypt(key, value)

    def decrypt(self, value):
        key = b'1234567890123456'
        return aes.decrypt(key, value)

    def __str__(self):
        return self.name


class Warehouse(db.Model):
    __tablename__ = 'warehouse'

    id_product = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False, primary_key=True)
    date_of_delivery = db.Column(db.Date, nullable=False)
    amount = db.Column(db.Integer, nullable=False)
    retail_price = db.Column(db.Integer, nullable=False)


class Sale(db.Model):
    __tablename__ = 'sales'
    id_product = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False, primary_key=True)
    date_sale = db.Column(db.DateTime, nullable=False)
    amount = db.Column(db.Integer, nullable=False)

    def __init__(self, id_product, date_sale, amount):
        self.id_product = id_product
        self.date_sale = self.encrypt(date_sale)
        self.amount = self.encrypt(amount)

    def encrypt(self, value):
        key = b'1234567890123456'
        return aes.encrypt(key, value)

    def decrypt(self):
        key = b'1234567890123456'
        return aes.decrypt(key, self.date_sale), aes.decrypt(key, self.amount)


class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), nullable=False)
    user = db.relationship('User', backref='roles')

    def __str__(self):
        return self.name


class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True, unique=True)
    name = db.Column(db.String(100), nullable=False)
    password_hash = db.Column(db.String(128))
    role_id = db.Column(db.Integer,db.ForeignKey('roles.id'), nullable=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __str__(self):
        return self.name

