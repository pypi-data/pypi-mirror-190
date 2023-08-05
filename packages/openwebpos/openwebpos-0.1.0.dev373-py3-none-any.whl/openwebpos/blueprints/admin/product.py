from flask import Blueprint, render_template, redirect, url_for, request

from openwebpos.forms.admin import ProductForm, ProductVariantForm
from openwebpos.models.admin import Product, ProductVariant
from openwebpos.utils.money import dollars_to_cents

product_view = Blueprint('product', __name__, template_folder='templates')


@product_view.route('/')
@product_view.route('/all')
def index():
    form = ProductForm()
    form.set_choices()
    products = Product.query.filter_by(active=True).all()
    return render_template('admin/product/all.html', products=products, form=form)


@product_view.route('/<string:product_name>', methods=['GET', 'POST'])
def product(product_name):
    _product = Product.query.filter_by(name=product_name).first()
    form = ProductForm(obj=_product)
    return render_template('admin/product/product.html', product=_product, form=form)


@product_view.post('/create')
def create_product():
    form = ProductForm()
    form.set_choices()
    if form.validate_on_submit():
        new_product = Product()
        form.populate_obj(new_product)
        new_product.price = dollars_to_cents(new_product.price)
        new_product.name = new_product.name.title()
        new_product.save()
    return redirect(url_for('.index'))


@product_view.post('/delete')
def delete_product():
    product = Product.query.get(request.form.get('product_id'))
    product.delete()
    return redirect(url_for('.index'))


@product_view.route('/<string:product_name>/edit', methods=['GET', 'POST'])
def edit_product(product_name):
    product = Product.query.filter_by(name=product_name).first()
    product_variants = product.product_variants
    form = ProductForm(obj=product)

    variant_form = ProductVariantForm(product_id=product.id)

    if form.validate_on_submit():
        form.populate_obj(product)
        product.price = dollars_to_cents(product.price)
        product.update()
        if product_variants:

            for variant in product_variants:

                if product.price > variant.price:
                    variant.price = product.price

                if product.price < variant.price:
                    lowest_variant = min(product_variants, key=lambda x: x.price)
                    product.price = lowest_variant.price
                    product.update()

                variant.update()

        return redirect(url_for('.edit_product', product_name=product.name))

    return render_template('admin/edit_product.html', product=product, form=form, variant_form=variant_form,
                           product_variants=product_variants)


@product_view.post('/add_variant')
def add_variant():
    variant_form = ProductVariantForm(product_id=request.form.get('product_id'))
    if variant_form.validate_on_submit():
        new_variant = ProductVariant()
        variant_form.populate_obj(new_variant)
        new_variant.price = dollars_to_cents(new_variant.price)
        new_variant.save()
        return redirect(url_for('.edit_product', product_name=new_variant.product.name))
    return redirect(url_for('.index'))


@product_view.post('/update_variant')
def update_variant():
    variant = ProductVariant.query.get(request.form.get('variant_id'))
    variant_name = request.form.get('variant_name')
    variant_price = request.form.get('variant_price')
    if request.method == 'POST':
        variant.name = variant_name
        variant.price = dollars_to_cents(float(variant_price))
        variant.update()
        return redirect(url_for('.edit_product', product_name=variant.product.name))
    return redirect(url_for('.index'))


@product_view.post('/delete_variant')
def delete_variant():
    variant = ProductVariant.query.filter_by(id=request.form.get('variant_id')).first()
    product = variant.product
    print(variant)
    if request.method == 'POST':
        variant.delete()
    return redirect(url_for('.edit_product', product_name=product.name))
