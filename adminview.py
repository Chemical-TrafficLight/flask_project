import flask_admin as fladmin
import flask_login as login
from flask import redirect, url_for
from flask_admin import helpers, expose
from models import User, Order
from flask_admin.contrib.sqla import ModelView


class MyAdminIndexView(fladmin.AdminIndexView):

    @expose('/')
    def index(self):
        if not login.current_user.is_authenticated:
            return redirect(url_for('login'))
        else:
            admin = User.query.filter(User.id == login.current_user.get_id()).first()
            if admin.role == 1:
                return super(MyAdminIndexView, self).index()
            return redirect(url_for('login'))


class MyModelView(ModelView):
    column_hide_backrefs = False

    def is_accessible(self):
        """
        This method used to check is current user is authenticated and his role is Admin
        :return:
        """
        if not login.current_user.is_authenticated:
            return False
        else:
            admin = User.query.filter(User.id == login.current_user.get_id()).first()
            if admin.role == 1:
                return True
            return False


class OrderView(MyModelView):

    column_list = ("id", "user_id", "date", "cart", "total")
    column_searchable_list = ["date"]
    column_sortable_list = ["date"]


class ProductsView(MyModelView):

    column_list = ("id", "name", "price", "orders")
    column_searchable_list = ["name", "price"]
    column_sortable_list = ["name"]