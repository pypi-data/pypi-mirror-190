from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, SubmitField, TextAreaField, FloatField, HiddenField
from wtforms.validators import DataRequired, Length, Email

from openwebpos.models.admin import ProductType, Product


class CompanyForm(FlaskForm):
    name = StringField('Company Name', validators=[DataRequired(), Length(min=2, max=50)])
    address = StringField('Address', validators=[DataRequired(), Length(min=2, max=50)])
    city = StringField('City', validators=[DataRequired(), Length(min=2, max=50)])
    state = StringField('State', validators=[DataRequired(), Length(min=2, max=50)])
    zip_code = StringField('Zipcode', validators=[DataRequired(), Length(min=2, max=50)])
    country = StringField('Country', validators=[DataRequired(), Length(min=2, max=50)])
    phone = StringField('Phone', validators=[DataRequired(), Length(min=10, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    website = StringField('Website', validators=[DataRequired(), Length(min=2, max=50)])
    tax_rate = StringField('Tax Rate', validators=[DataRequired(), Length(min=2, max=50)])
    submit = SubmitField('Update Company')


class ProductForm(FlaskForm):
    product_type_id = SelectField('Product Type', coerce=int)
    name = StringField('Name', validators=[DataRequired(), Length(min=2, max=50)])
    description = TextAreaField('Description', validators=[Length(max=128)])
    price = FloatField('Price', validators=[DataRequired()])

    def set_choices(self):
        """Set choices for product type select field."""
        self.product_type_id.choices = [(product_type.id, product_type.name) for product_type in
                                        ProductType.query.filter_by(active=True).all()]

    def __init__(self, *args, **kwargs):
        super(ProductForm, self).__init__(*args, **kwargs)
        self.set_choices()


class ProductVariantForm(FlaskForm):
    product_id = HiddenField('product_id')
    name = StringField('Name', validators=[DataRequired(), Length(min=2, max=50)])
    price = FloatField('Price')

    def set_product_id(self, product_id):
        self.product_id.data = product_id

    def __init__(self, *args, **kwargs):
        super(ProductVariantForm, self).__init__(*args, **kwargs)
        self.set_product_id(kwargs['product_id'])
        product_price = Product.query.get(self.product_id.data).price
        if self.price.data is None:
            self.price.data = product_price / 100
