from app import db


class Product(db.Model):
    __tablename__ = 'products'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    shelf_life = db.Column(db.Date, nullable=False)
    trade_price = db.Column(db.Integer, nullable=False)

    id_unit = db.Column(db.Integer, db.ForeignKey('Unit.id'), nullable=False)
    id_category = db.Column(db.Integer, db.ForeignKey('Category.id'), nullable=False)
    id_supplier = db.Column(db.Integer, db.ForeignKey('Supplier.id'), nullable=False)

    sale = db.relationship('Sale', backref='sales')


class Unit(db.Model):
    __tablename__ = 'units'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    product = db.relationship('Product', backref='units')


class Category(db.Model):
    __tablename__ = 'categories'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    product = db.relationship('Product', backref='categories')
    supplier = db.relationship('Supplier', backref='suppliers')


class Supplier(db.Model):
    __tablename__ = 'suppliers'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    address = db.Column(db.Text, nullable=False)
    contacts = db.Column(db.Integer, nullable=False)
    contract_number = db.Column(db.Integer)

    id_category = db.Column(db.Integer, db.ForeignKey('Category.id'), nullable=False)


class Warehouse(db.Model):
    __tablename__ = 'warehouse'

    id_product = 0
    date_of_delivery = db.Column(db.Date, primary_key=True)
    amount = db.Column(db.Integer, nullable=False)
    retail_price = db.Column(db.Integer, nullable=False)


class Sale(db.Model):
    __tablename__ = 'sales'

    id_product = db.Column(db.Integer, db.ForeignKey('Product.id'), nullable=False)
    date_sale = db.Column(db.Date, primary_key=True)
    amount = db.Column(db.Integer, nullable=False)


class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), nullable=False)
    user = db.relationship('User', backref='roles')


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    role_id = db.Column(db.Integer,db.ForeignKey('Role.id'), nullable=False)

