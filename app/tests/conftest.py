import re
import pytest
import factory
import sqlalchemy.orm
from app.db.db import get_db
from app.models.models import Base, Category, PaymentMethods, Product, ProductDiscount, User, Supplier
from app.app import app
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from _pytest.python import Module

@pytest.fixture()
def db_session():
    engine = create_engine('sqlite:///./test.db',connect_args={'check_same_thread': False})
    Session = sessionmaker(bind=engine)
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
    yield Session()

@pytest.fixture()
def override_get_db(db_session):
    def _override_get_db():
        yield db_session
    return _override_get_db

@pytest.fixture()
def client(override_get_db):
    app.dependency_overrides[get_db] = override_get_db
    client = TestClient(app)
    return client

@pytest.fixture()
def user_factory(db_session):
    class UserFactory(factory.alchemy.SQLAlchemyModelFactory):
        class Meta:
            model = User
            sqlalchemy_session = db_session
        id = None
        display_name = factory.Faker('name')
        email = factory.Faker('email')
        role = None
        password = '$2b$12$2F.MmED.HUKwVq74djSzguVYu4HBYEkKYNqxRnc/.gVG24QyYcC9m'
    return UserFactory

@pytest.fixture()
def address_test(db_session):
    class address_test(factory.alchemy.SQLAlchemyModelFactory):
        class Test:
            model: Category
            sqlalchemy_session = db_session
        id = factory.Faker('pyint')
        address = factory.Faker('name')
        city = factory.faker('name')
        state = factory.faker('name')
        number = factory.faker('name')
        zipcode = factory.faker('name')
        neighbourhood = factory.faker('name')
        primary = factory.faker('name')
        customer_id = customer.id
        customer = factory.faker('')
    return address_test

@pytest.fixture()
def category_test(db_session):
    class Category_Test(factory.alchemy.SQLAlchemyModelFactory):
        class Test:
            model: Category
            sqlalchemy_session = db_session
        id = factory.Faker('pyint')
        name = factory.Faker('name')
    return Category_Test

@pytest.fixture()
def payment_test(db_session):
    class Payment_Test(factory.alchemy.SQLAlchemyModelFactory):
        class Test:
            model: PaymentMethods
            sqlalchemy_session = db_session
        id = factory.Faker('pyint')
        name = factory.Faker('name')
        enabled = True
    return Payment_Test

@pytest.fixture()
def product_test(db_session):
    class product_test(factory.alchemy.SQLAlchemyModelFactory):
        class Test:
            model: Product
            sqlalchemy_session = db_session
            id = factory.Faker('pyint')
            description =  factory.Faker('name')
            price = factory.Faker('pyfloat')
            technical_details = factory.Faker('name')
            image  = factory.Faker('name')
            visible = True
            category =  category.id
            supplier = supplier.id
    return product_test

@pytest.fixture()
def product_discount_test(db_session):
    class Product_Discount_Test(factory.alchemy.SQLAlchemyModelFactory):
        class Test:
            model: ProductDiscount
            sqlalchemy_session = db_session
        id = factory.Faker('pyint')
        name = factory.Faker('name')
        value = factory.Faker('pyfloat')
        product =  factory.SubFactory('')
        payment_method =  factory.SubFactory('')
    return Product_Discount_Test

@pytest.fixture()
def supplier_test(db_session):
    class supplier_test(factory.alchemy.SQLAlchemyModelFactory):
        class Test:
            model: Category
            sqlalchemy_session = db_session
        id = factory.Faker('pyint')
        name = factory.Faker('name')
    return supplier_test

@pytest.fixture()
def user_admin_token(user_factory):
    user_factory(role='admin')
    return 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6MSwiZXhwIjoxNjY1NDIwODc0fQ.o_syoOwrg8VOvl5nWYnA0waXxL0pFLdUgJY8HoqMVjM'

@pytest.fixture()
def admin_auth_header(user_admin_token):
    return {'Authorization': f'Bearer {user_admin_token}'}
