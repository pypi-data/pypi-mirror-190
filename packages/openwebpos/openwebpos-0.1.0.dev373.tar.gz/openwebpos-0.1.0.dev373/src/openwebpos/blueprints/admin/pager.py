from flask import Blueprint, render_template, request, redirect, url_for

from openwebpos.models.admin import Pager

pager_view = Blueprint('pager', __name__)


@pager_view.route('/')
def index():
    pagers = Pager.query.all()
    return render_template('admin/pager/index.html', pagers=pagers)


@pager_view.post('/create')
def create_pager():
    if request.method == 'POST':
        pager = Pager(name=request.form['name'])
        pager.save()
    return redirect(url_for('.index'))


@pager_view.post('/update')
def update_pager():
    if request.method == 'POST':
        pager = Pager.query.filter_by(name=request.form['name']).first()
        name = request.form['name']
        if request.form.get('active'):
            active = True
        else:
            active = False

        pager.name = name
        pager.active = active
        pager.update()
    return redirect(url_for('.index'))


@pager_view.post('/delete')
def delete_pager():
    if request.method == 'POST':
        pager = Pager.query.filter_by(id=request.form['id']).first()
        pager.delete()
    return redirect(url_for('.index'))
