from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

db = SQLAlchemy()
metadata = db.metadata


class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(300), nullable=False)
    role = db.Column(db.Integer, db.ForeignKey('roles.id'),
                     nullable=False)  # внешний ключ для связи 1 ко многим с моделью Roles(у 1 роли много пользователей, у 1 пользователя 1 роль)
    orders = db.relationship("Order", backref="orders", lazy=True,
                             cascade="all,delete-orphan")  # отношения для связи многие к одному к модели Orders


class Roles(db.Model):
    """
    Модель таблицы Roles
    Связана с моделью User
    """
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    users = db.relationship('User', backref='user', lazy=True,
                            cascade="all, delete-orphan", )  # отношение 1 ко многим с моделью Users


# Связная таблица для связи многие ко многим
cart = db.Table('cart',
                db.Column('products', db.Integer, db.ForeignKey('products.id')),
                db.Column('orders', db.Integer, db.ForeignKey('orders.id')),
                )


class Products(db.Model):
    """
    Модель таблицы products
    Связана с моделью Orders
    """
    __tablename__ = 'products'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)
    orders = db.relationship("Order", secondary=cart, back_populates="cart")  # связь многие ко многим,
    # атрибут back_populates указывает на какой атрибут в связной таблице мы будем ссылаться при обращении(должен быть равен имени переменной в другой таблице)
    # нужен для того чтобы получить список заказов для товара

    def __repr__ (self):
        """
        Репрезентативный магический метод
        нужен для представления объекта класса человеческим языком(а не <class object in 0x88005553535>)

        :return: Название товара
        """

        return self.name


class Order(db.Model):
    """
    Модель таблицы orders
    Связана с моделью Products
    """
    __tablename__ = 'orders'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    cart = db.relationship("Products", secondary=cart, back_populates="orders")
    date = db.Column(db.DateTime)
    total = db.Column(db.Float, nullable=False)

    def __repr__ (self):
        """
        Репрезентативный магический метод
        нужен для представления объекта класса человеческим языком(а не <class object in 0x88005553535>)

        :return: id заказа
        """

        return str(self.id)