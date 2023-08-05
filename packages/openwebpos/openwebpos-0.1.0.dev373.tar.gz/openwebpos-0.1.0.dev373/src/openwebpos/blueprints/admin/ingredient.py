from flask import Blueprint, render_template, request, redirect, url_for

from openwebpos.models.admin import Ingredient

ingredient_view = Blueprint('ingredient', __name__, template_folder='templates')


@ingredient_view.route('/')
def index():
    ingredients = Ingredient.query.all()
    return render_template('admin/ingredient/index.html', ingredients=ingredients)


@ingredient_view.post('/remove')
def remove_ingredient():
    if request.method == 'POST':
        ingredient = Ingredient.query.filter_by(id=request.form['ingredient_id']).first()
        ingredient.delete()
    return redirect(url_for('.index'))


@ingredient_view.post('/update')
def update_ingredient():
    if request.method == 'POST':
        ingredient = Ingredient.query.filter_by(id=request.form['ingredient_id']).first()
        name = request.form['name']
        if request.form.get('active'):
            active = True
        else:
            active = False

        ingredient.name = name
        ingredient.active = active
        ingredient.update()
    return redirect(url_for('.index'))


@ingredient_view.post('/create')
def create_ingredient():
    if request.method == 'POST':
        ingredient = Ingredient(name=request.form['name'])
        ingredient.save()
    return redirect(url_for('.index'))
