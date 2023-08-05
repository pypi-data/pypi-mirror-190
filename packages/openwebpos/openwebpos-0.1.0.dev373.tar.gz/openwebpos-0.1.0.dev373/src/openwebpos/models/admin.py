from flask_login import current_user

from ..extensions import db
from ..utils import gen_order_number
from ..utils.sql import CRUDMixin


class Company(CRUDMixin, db.Model):
    name = db.Column(db.String(64), unique=True, index=True)
    address = db.Column(db.String(128))
    city = db.Column(db.String(64))
    state = db.Column(db.String(64))
    zip_code = db.Column(db.String(64))
    country = db.Column(db.String(64))
    phone = db.Column(db.String(64))
    email = db.Column(db.String(64))
    website = db.Column(db.String(64))
    logo = db.Column(db.String(64))
    tax_rate = db.Column(db.Integer, default=0)

    @classmethod
    def insert_default_data(cls):
        company = Company(name='Company Name',
                          address='123 Main Street',
                          city='City',
                          state='State',
                          zip_code='12345',
                          country='Country',
                          phone='123-456-7890',
                          email='info@mail.com',
                          website='www.website.com',
                          logo='logo.png',
                          tax_rate=825)
        company.save()

    def __init__(self, **kwargs):
        super(Company, self).__init__(**kwargs)


class PaymentMethod(CRUDMixin, db.Model):
    name = db.Column(db.String(64), unique=True, index=True)
    active = db.Column(db.Boolean, default=True)

    def __init__(self, **kwargs):
        super(PaymentMethod, self).__init__(**kwargs)

    def is_active(self):
        return self.active

    @classmethod
    def insert_default_data(cls):
        methods = ['Cash', 'Credit Card', 'Check', 'Gift Card', 'Other']
        for method in methods:
            payment_method = PaymentMethod(name=method)
            payment_method.save()


class Pager(CRUDMixin, db.Model):
    name = db.Column(db.String(64), unique=True)
    in_use = db.Column(db.Boolean, default=False)
    active = db.Column(db.Boolean, default=True)

    @classmethod
    def insert_default_data(cls):
        pagers = ['Pager 1', 'Pager 2', 'Pager 3', 'Pager 4', 'Pager 5', 'Pager 6', 'Pager 7', 'Pager 8', 'Pager 9',
                  'Pager 10']
        for pager in pagers:
            pager = Pager(name=pager)
            pager.save()

    @classmethod
    def toggle_in_use(cls, name):
        pager = cls.query.filter_by(name=name).first()
        pager.in_use = not pager.in_use
        pager.update()

    def is_in_use(self):
        return self.in_use

    def __init__(self, **kwargs):
        super(Pager, self).__init__(**kwargs)


class OrderType(CRUDMixin, db.Model):
    __tablename__ = 'order_types'
    name = db.Column(db.String(64), unique=True, index=True)
    active = db.Column(db.Boolean, default=True)

    @classmethod
    def insert_default_data(cls):
        types = ['Dine In', 'Take Out', 'Delivery', 'Phone']
        for type in types:
            order_type = OrderType(name=type)
            order_type.save()

    def __init__(self, **kwargs):
        super(OrderType, self).__init__(**kwargs)


class Order(CRUDMixin, db.Model):
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    created_by = db.Column(db.Integer, nullable=False)
    order_type_id = db.Column(db.Integer, nullable=False)
    order_number = db.Column(db.String(24), unique=True, index=True)
    pager = db.Column(db.String(64), nullable=True)
    subtotal = db.Column(db.Integer, default=0)
    tax = db.Column(db.Integer, default=0)
    active = db.Column(db.Boolean, default=True)

    # ***** ---Relationships--- *****
    order_items = db.relationship('OrderItem', backref='order', lazy=True, cascade="all, delete-orphan")

    @classmethod
    def created_by_user(cls, user_id):
        return cls.query.filter_by(created_by=user_id, active=True).all()

    @classmethod
    def create_order(cls, order_type_id, pager, user_id=None):
        order = Order(order_type_id=order_type_id, pager=pager, user_id=user_id)
        order.save()
        if pager:
            Pager.toggle_in_use(pager)
        return order

    @classmethod
    def get_last_order_number_by_user(cls, user_id):
        order = cls.query.filter_by(created_by=user_id, active=True).order_by(cls.id.desc()).first()
        if order:
            return order.order_number
        else:
            return None

    @classmethod
    def update_totals(cls, order_id):
        order = cls.query.get(order_id)
        order_items = OrderItem.query.filter_by(order_id=order_id).all()
        order.subtotal = 0
        for item in order_items:
            order.subtotal += item.price * item.quantity
        order.tax = int(order.subtotal * Company.query.first().tax_rate / 10000)
        order.update()

    def __init__(self, **kwargs):
        super(Order, self).__init__(**kwargs)
        self.order_number = gen_order_number()
        self.created_by = current_user.id
        if self.user_id is None:
            self.user_id = 5  # Guest user

        if self.pager is None:
            self.pager = self.order_type_id.name


class OrderItem(CRUDMixin, db.Model):
    product_name = db.Column(db.String(64), index=True, nullable=False)
    product_variant_name = db.Column(db.String(64), index=True)
    quantity = db.Column(db.Integer, default=1)
    price = db.Column(db.Integer, default=0)

    # ***** ---Relationships--- *****
    order_id = db.Column(db.Integer, db.ForeignKey('order.id'), nullable=False)

    @classmethod
    def insert_data(cls, o_id, p_name, v_name, qty, price):
        if v_name is None:
            v_name = ''
        order_item = OrderItem(order_id=o_id, product_name=p_name, product_variant_name=v_name,
                               quantity=qty, price=price)
        order_item.save()
        Order.update_totals(o_id)

    @classmethod
    def update_item_quantity(cls, order_id, ordered_item_id, quantity):
        order_item = cls.query.get(ordered_item_id)
        order_item.quantity = quantity
        order_item.update()
        Order.update_totals(order_id)

    @classmethod
    def remove_item_from_order(cls, order_id, ordered_item_id):
        order_item = cls.query.get(ordered_item_id)
        order_item.delete()
        Order.update_totals(order_id)

    def __init__(self, **kwargs):
        super(OrderItem, self).__init__(**kwargs)


class ProductType(CRUDMixin, db.Model):
    __tablename__ = 'product_types'
    name = db.Column(db.String(64), unique=True, index=True)
    active = db.Column(db.Boolean, default=True)

    # ***** ---Relationships--- *****
    products = db.relationship('Product', backref='product_type', lazy=True, cascade="all, delete-orphan")

    @classmethod
    def insert_default_data(cls):
        types = ['Food', 'Beverage', 'Desert', 'Other']
        for t in types:
            product_type = ProductType(name=t)
            product_type.save()

    def __init__(self, **kwargs):
        super(ProductType, self).__init__(**kwargs)


product_ingredients = db.Table('product_ingredients',
                               db.Column('product_id', db.Integer, db.ForeignKey('product.id'), primary_key=True),
                               db.Column('ingredient_id', db.Integer, db.ForeignKey('ingredient.id'), primary_key=True)
                               )


class Product(CRUDMixin, db.Model):
    name = db.Column(db.String(64), unique=True, index=True)
    description = db.Column(db.String(128))
    price = db.Column(db.Integer, default=0)
    active = db.Column(db.Boolean, default=True)

    # ***** ---Relationships--- *****
    product_type_id = db.Column(db.Integer, db.ForeignKey('product_types.id'), nullable=False)
    product_variants = db.relationship('ProductVariant', backref='product', lazy='joined', cascade="all, delete-orphan")
    ingredients = db.relationship('Ingredient', secondary=product_ingredients, lazy='subquery',
                                  backref=db.backref('products', lazy=True))

    @classmethod
    def has_variants(cls, product_id):
        product = Product.query.get(product_id)
        if product.product_variants:
            return True
        else:
            return False

    @classmethod
    def get_product_variants(cls, product_id):
        product = Product.query.get(product_id)
        if product.product_variants:
            return product.product_variants
        else:
            return None

    @classmethod
    def insert_default_data(cls):
        products = [
            {'name': 'Burger', 'description': 'A delicious burger', 'price': 1000, 'product_type_id': 1},
            {'name': 'Fries', 'description': 'A delicious fries', 'price': 500, 'product_type_id': 1},
            {'name': 'Soda', 'description': 'A delicious soda', 'price': 200, 'product_type_id': 2},
        ]
        for p in products:
            product = Product(name=p['name'], description=p['description'], price=p['price'],
                              product_type_id=p['product_type_id'])
            product.save()

    def __init__(self, **kwargs):
        super(Product, self).__init__(**kwargs)


class ProductVariant(CRUDMixin, db.Model):
    __tablename__ = 'product_variants'
    name = db.Column(db.String(64), index=True)
    price = db.Column(db.Integer, default=0)
    active = db.Column(db.Boolean, default=True)

    # ***** ---Relationships--- *****
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)

    def __init__(self, **kwargs):
        super(ProductVariant, self).__init__(**kwargs)


class Ingredient(CRUDMixin, db.Model):
    name = db.Column(db.String(64), unique=True)
    active = db.Column(db.Boolean, default=True)

    @classmethod
    def insert_default_data(cls):
        ingredients = [
            {'name': 'Lettuce'},
            {'name': 'Bun'},
            {'name': 'Tomato'},
            {'name': 'Patty'},
            {'name': 'Onion'},
            {'name': 'Cheese'}
        ]
        for i in ingredients:
            ingredient = Ingredient(name=i['name'])
            ingredient.save()

    @classmethod
    def toggle_active(cls, ingredient_id):
        ingredient = Ingredient.query.get(ingredient_id)
        ingredient.active = not ingredient.active
        ingredient.update()

    def __init__(self, **kwargs):
        super(Ingredient, self).__init__(**kwargs)
