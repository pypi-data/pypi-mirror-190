from flask import Blueprint, render_template
from openwebpos.forms.admin import CompanyForm
from openwebpos.models.admin import Company

from .ingredient import ingredient_view
from .pager import pager_view
from .product import product_view

admin_view = Blueprint('admin', __name__, template_folder='templates')
admin_view.register_blueprint(product_view, url_prefix='/product')
admin_view.register_blueprint(pager_view, url_prefix='/pager')
admin_view.register_blueprint(ingredient_view, url_prefix='/ingredient')


@admin_view.route('/')
def index():
    return render_template('admin/index.html')


@admin_view.route('/company', methods=['GET', 'POST'])
def company_route():
    company = Company.query.first()
    form = CompanyForm(obj=company)
    if form.validate_on_submit():
        form.populate_obj(company)
        company.update()
    return render_template('admin/company.html', company=company, form=form)


@admin_view.get('/products')
def products():
    return render_template('admin/products.html')
