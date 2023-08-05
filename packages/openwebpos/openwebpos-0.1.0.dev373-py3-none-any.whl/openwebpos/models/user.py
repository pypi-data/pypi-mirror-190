from datetime import datetime

from flask_login import UserMixin, current_user
from werkzeug.security import generate_password_hash, check_password_hash

from openwebpos.extensions import db
from openwebpos.utils.sql import CRUDMixin, DateTimeMixin

role_permissions = db.Table('role_permissions',
                            db.Column('permission_id', db.Integer, db.ForeignKey('permission.id')),
                            db.Column('role_id', db.Integer, db.ForeignKey('role.id'))
                            )


class Role(CRUDMixin, db.Model):
    """
    User Role Model.
    """
    name = db.Column(db.String(40), unique=True, nullable=False)
    users = db.relationship('User', backref='role', lazy=True)
    permissions = db.relationship('Permission', secondary=role_permissions, backref=db.backref('roles', lazy='select'))

    # ***** Relationships *****
    # ***** ---Children--- *****

    def has_permission(self, permission):
        """
        Check if the role has a specific permission.

        Args:
            permission (str): Permission name.

        Returns:
            bool: True if the role has the permission, False otherwise.
        """
        return self.permissions.filter_by(name=permission).first() is not None

    @staticmethod
    def insert_roles():
        """
        Insert roles into the database.
        """
        roles = [
            {'name': 'admin'},
            {'name': 'manager'},
            {'name': 'employee'},
            {'name': 'customer'},
            {'name': 'guest'}
        ]
        for r in roles:
            role = Role.query.filter_by(name=r['name']).first()
            if role is None:
                role = Role(**r)
                role.save()

    def __init__(self, **kwargs):
        super(Role, self).__init__(**kwargs)
        self.name = kwargs.get('name').title()


class Permission(CRUDMixin, db.Model):
    """
    User Permission Model.
    """
    name = db.Column(db.String(40), unique=True, nullable=False)

    def __init__(self, **kwargs):
        super(Permission, self).__init__(**kwargs)
        self.name = kwargs.get('name').title()


class User(CRUDMixin, DateTimeMixin, UserMixin, db.Model):
    """
    User Model.
    """
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    active = db.Column(db.Boolean, default=True, nullable=False)

    # ***** Relationships *****
    # ***** ---Parent---  *****
    role_id = db.Column(db.Integer, db.ForeignKey('role.id'), nullable=False)

    # ***** ---Children--- *****
    profile = db.relationship('Profile', backref='user', lazy='joined', uselist=False, cascade='all, delete-orphan')
    activity = db.relationship('Activity', backref='user', lazy=True, uselist=False, cascade='all, delete-orphan')
    orders = db.relationship('Order', backref='user', lazy=True, cascade='all, delete-orphan')

    def verify_password(self, password):
        """
        Verify the user password.
        """
        return check_password_hash(self.password, password)

    def has_role(self, role):
        """
        Check if the user has the specified role.
        """
        return self.role.name == role.title()

    @staticmethod
    def insert_users():
        """
        Insert users into the database.
        """
        users = [
            {'username': 'admin', 'password': 'admin', 'role_id': 1},
            {'username': 'manager', 'password': 'manager', 'role_id': 2},
            {'username': 'employee', 'password': 'employee', 'role_id': 3},
            {'username': 'customer', 'password': 'customer', 'role_id': 4},
            {'username': 'guest', 'password': 'guest', 'role_id': 5},
        ]
        for u in users:
            user = User.query.filter_by(username=u['username']).first()
            if user is None:
                un = u['username'].title()
                user = User(username=un, password=u['password'], role_id=u['role_id'])
            user.save()

    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)
        self.password = generate_password_hash(kwargs.get('password'))
        if self.role_id is None:
            self.role_id = Role.query.filter_by(name='User').first().id


class Profile(CRUDMixin, db.Model):
    __tablename__ = 'user_profile'
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    picture = db.Column(db.String(255), nullable=True, default='default.png')
    first_name = db.Column(db.String(120))
    last_name = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    address = db.Column(db.String(120))
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    zip_code = db.Column(db.String(120))
    dob = db.Column(db.String(120))

    def __init__(self, **kwargs):
        super(Profile, self).__init__(**kwargs)


class Activity(CRUDMixin, db.Model):
    __tablename__ = 'user_activity'

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    sign_in_count = db.Column(db.Integer, nullable=False, default=0)
    current_sign_in_at = db.Column(db.DateTime, nullable=True)
    current_sign_in_ip = db.Column(db.String(100), nullable=True)
    last_sign_in_at = db.Column(db.DateTime, nullable=True, default=None)
    last_sign_in_ip = db.Column(db.String(100), nullable=True, default=None)
    user_agent = db.Column(db.String(120))
    referrer = db.Column(db.String(120))

    def __init__(self, **kwargs):
        super(Activity, self).__init__(**kwargs)

    def update_activity(self, user_agent: str, referrer: str, ip_address: str):
        """
        Update the user activity.
        """
        self.user_id = current_user.id
        self.user_agent = user_agent
        self.referrer = referrer
        self.last_sign_in_at = self.current_sign_in_at
        self.last_sign_in_ip = self.current_sign_in_ip
        self.current_sign_in_at = datetime.utcnow()
        self.current_sign_in_ip = ip_address
        if self.sign_in_count is None:
            self.sign_in_count = 0
        else:
            self.sign_in_count += 1

        return self.update()
