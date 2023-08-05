from flask import Blueprint, render_template, request, redirect, url_for, session
from flask_login import login_required, current_user

from openwebpos.decorators.user import role_required
from openwebpos.models.admin import Order, OrderType, Product, Pager, OrderItem

pos_view = Blueprint('pos', __name__, template_folder='templates')


@pos_view.before_request
@login_required
@role_required('Admin', 'Manager', 'Employee')
def before_request():
    """
    Secure all pos/ routes.
    """
    pass


@pos_view.route('/')
def index():
    allowed_roles = ['Admin', 'Manager']
    order_types = OrderType.query.filter_by(active=True).all()
    pagers = Pager.query.filter_by(active=True, in_use=False).all()
    active_orders = Order.created_by_user(current_user.id)

    if current_user.role.name in allowed_roles:
        active_orders = Order.query.filter_by(active=True).all()

    if active_orders:
        return render_template('pos/active_orders.html', active_orders=active_orders, pagers=pagers,
                               order_types=order_types)

    return render_template('pos/index.html', order_types=order_types, pagers=pagers)


@pos_view.post('/')
def create_order():
    # if request.form.get('pager_name') != 'None':
    Order.create_order(order_type_id=request.form['order_type_id'], pager=request.form['pager_name'])
    session['order'] = Order.get_last_order_number_by_user(current_user.id)
    return redirect(url_for('.order'))
    # return redirect(url_for('.index'))


@pos_view.route('/order')
def order():
    _order = session.get('order', None)
    current_order = Order.query.filter_by(order_number=session.get('order', None)).first()
    current_ordered_items = OrderItem.query.filter_by(order_id=current_order.id).all()
    products = Product.query.filter_by(active=True).all()
    return render_template('pos/order.html', order_number=_order, current_ordered_items=current_ordered_items,
                           products=products, current_order=current_order)


@pos_view.post('/add_product')
def add_product():
    # _order = Order.query.filter_by(order_number=order_number).first()
    _order = Order.query.filter_by(order_number=session.get('order', None)).first()
    if request.method == 'POST':

        product_name = request.form.get('product_name')
        quantity = request.form.get('quantity')

        if request.form.get('product_variant_name'):
            product_variant_name = request.form.get('product_variant_name')
            product_variant_price = request.form.get('product_variant_price')
            OrderItem.insert_data(o_id=_order.id, p_name=product_name, v_name=product_variant_name, qty=quantity,
                                  price=product_variant_price)
        else:
            product_price = request.form.get('product_price')
            OrderItem.insert_data(o_id=_order.id, p_name=product_name, v_name=None, qty=quantity, price=product_price)
    return redirect(url_for('.order'))


@pos_view.post('/update_product_quantity')
def update_product_quantity():
    _order = Order.query.filter_by(order_number=session.get('order', None)).first()
    if request.method == 'POST':
        ordered_item_id = request.form.get('ordered_item_id')
        quantity = request.form.get('quantity')
        OrderItem.update_item_quantity(ordered_item_id=ordered_item_id, order_id=_order.id, quantity=quantity)
    return redirect(url_for('.order'))


@pos_view.post('/remove_product')
def remove_product():
    _order = Order.query.filter_by(order_number=session.get('order', None)).first()
    if request.method == 'POST':
        ordered_item_id = request.form.get('ordered_item_id')
        OrderItem.remove_item_from_order(ordered_item_id=ordered_item_id, order_id=_order.id)
    return redirect(url_for('.order'))
