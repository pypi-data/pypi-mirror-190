import os.path

from flask import Blueprint, render_template, redirect, url_for, current_app, request
from flask_login import login_user, current_user, logout_user

from .admin import admin_view
from .pos import pos_view
from ..forms import LoginForm
from ..models.admin import Company, PaymentMethod, OrderType, ProductType, Product, Pager, Ingredient
from ..models.user import User, Role, Activity

core_bp = Blueprint('route', __name__, template_folder='templates')

core_bp.register_blueprint(pos_view, url_prefix='/pos')
core_bp.register_blueprint(admin_view, url_prefix='/admin')


def insert_default_data():
    """
    Insert default data.
    """
    Role.insert_roles()
    User.insert_users()
    Company.insert_default_data()
    PaymentMethod.insert_default_data()
    OrderType.insert_default_data()
    ProductType.insert_default_data()
    Product.insert_default_data()
    Pager.insert_default_data()
    Ingredient.insert_default_data()


@core_bp.route('/')
def index():
    if current_app.config.get('DB_CONFIGURED') is False:
        sqlite_path = current_app.config.get('APP_PATH')
        sqlite_name = 'openwebpos.db'
        return render_template('configure_database.html', sqlitePath=sqlite_path, sqliteName=sqlite_name)

    if current_app.config.get('APP_RESTARTED') is False:
        return render_template('restart.html')

    if User.query.filter_by(username='Admin').first() is None:
        insert_default_data()

    return redirect(url_for('.pos.index'))


@core_bp.post('/setup/sqlite')
def setup_sqlite():
    if request.method == 'POST':
        sqlite_path = request.form.get('sqlitePath')
        sqlite_name = request.form.get('sqliteName')
        env_path = current_app.config.get('APP_ENV_PATH')
        current_app.config.update(DB_CONFIGURED=True)
        with open(os.path.join(env_path, '.env'), 'w') as f:
            f.write("APP_RESTARTED=True\r")
            f.write("DB_CONFIGURED=True\r")
            f.write("DB_DIALECT=sqlite\r")
            f.write(f"SQLALCHEMY_DATABASE_URI=sqlite:///{sqlite_path}/{sqlite_name}")
    return redirect(url_for('.index'))


@core_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('.index'))

    form = LoginForm()

    if form.validate_on_submit():
        form_username = form.username.data
        user = User.query.filter_by(username=form_username.title()).first()
        if user is not None and user.verify_password(form.password.data):
            if user.is_active:
                login_user(user)
                user_agent = request.headers.get('User-Agent')
                referrer = request.referrer
                ip_address = request.remote_addr
                user_activity = Activity.query.filter_by(user_id=user.id).first()
                if user_activity is None:
                    user_activity = Activity(user_id=user.id)
                    user_activity.update_activity(user_agent, referrer, ip_address)
                    user_activity.save()
                user_activity.update_activity(user_agent, referrer, ip_address)

            return redirect(url_for('.index'))
    return render_template('login.html', form=form)


@core_bp.get('/logout')
def logout():
    logout_user()
    return redirect(url_for('.index'))


@core_bp.route('/ddb')
def ddb():
    from ..extensions import db
    db.drop_all()
    db.create_all()
    insert_default_data()
    return redirect(url_for('.index'))
