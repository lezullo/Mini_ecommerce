from datetime import datetime
from typing import List
from fastapi import HTTPException, status
from fastapi.param_functions import Depends
from app.api.order.schemas import OrderSchema, ProductSchema, ProductSchema, OrderSchema, OrderStatus, OrderStatusSchema, OrderProductSchema
from app.api.coupons.schemas import CouponType
from app.models.models import OrderProducts, OrderStatus, Order, User
from app.repositories.order_repository import OrderRepository
from app.repositories.order_status_repository import OrderStatusRepository
from app.repositories.order_product_repository import OrderProductRepository
from app.repositories.custumer_repository import CustomerRepository
from app.repositories.product_repository import ProductRepository
from app.repositories.adress_repository import AddressRepository
from app.services.coupons_service import CouponsService
from random import randint

class OrderService:
    def __init__(self, order_repository: OrderRepository = Depends(),
                order_product_repository: OrderProductRepository = Depends(),
                order_status_repository : OrderStatusRepository = Depends(),
                product_repository: ProductRepository = Depends(),
                customer_repository: CustomerRepository = Depends(),
                address_repository: AddressRepository = Depends(),
                coupon_service: CouponsService = Depends()) -> None:
        self.order_repository = order_repository
        self.order_product_repository = order_product_repository
        self.order_status_repository = order_status_repository
        self.product_repository = product_repository
        self.customer_repository = customer_repository
        self.addresses_repository = address_repository
        self.coupon_service = coupon_service

    def create(self, input_order_schema: OrderSchema, user: User):
        order_schema = OrderSchema()
        order_schema.number = randint(0, 9999)
        order_schema.status = OrderStatus.ORDER_PLACED
        order_schema.created_at = datetime.now()
        order_schema.payment_form_id = input_order_schema.payment_form_id
        order_schema.customer_id = self.get_customer_id(user.id)
        order_schema.address_id = input_order_schema.address_id
        order_schema.total_value = self.get_products_value(input_order_schema.products)
        order_schema.total_discount = self.get_discount_value(input_order_schema.coupon_code, order_schema.total_value)
        self.validate_address(order_schema.customer_id, order_schema.address_id)
        self.order_repository.create(Order(**order_schema.dict()))
        id_order = self.order_repository.get_by_number(order_schema.number).id
        self.create_order_status(id_order,OrderStatus.ORDER_PLACED)
        self.create_order_products(id_order,input_order_schema.products)

    def create_order_status(self, id_order: int, current_status: OrderStatus):
        self.order_status_repository.create(OrderStatus(**OrderStatusSchema(id_order,current_status,datetime.now()).__dict__))
    
     def get_products_value(self, products: List[ProductSchema]):        
        value: float = 0.00
        for product in products:
            query = self.products_repository.get_by_id(product.id)
            if not query:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='invalid product')
            value += (float(query.price) * product.quantity)
        return value

    def get_discount_value(self, code: str, total_value: float):
        query = self.coupon_service.query_valid_by_code(code)
        if query:
            if query.type == CouponType.VALUE:
                return query.value
            if query.type == CouponType.PERCENTAGE:
                return (query.value/100)*total_value
        return 0
   
    def validate_address(self, customer_id, address_id):
        query = self.addresses_repository.get_by_id(address_id) 
        if not query or query.customer_id != customer_id:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Inválid address')

    def get_address_id(self, id: int):
        return self.addresses_repository.get_by_customer_id(id).id

    def get_customer_id(self, id: int):
        return self.customer_repository.get_by_user_id(id).id

    def create_order_products(self, id_order: int, products: List[ProductSchema]):
        for product in products:
            self.order_product_repository.create(OrderProducts(**OrderProductSchema(id_order, product.id, product.quantity).__dict__))
            
    def update(self, id:int, order_status:OrderStatus):
        self.order_repository.update(id,{'status':f'{order_status}'})
        self.create_order_status(id, order_status)
