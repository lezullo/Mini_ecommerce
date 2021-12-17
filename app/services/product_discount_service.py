from fastapi import Depends
from app.api.product_discount.schemas import ProductDiscountSchema
from app.api.repositories.payment_method_repository import PaymentMethodRepository
from app.api.repositories.product_discount_repository import ProductDiscountRepository
from app.models.models import Product, PaymentMethods, ProductDiscount

from fastapi.exceptions import HTTPException
from fastapi import status

class ProductDiscountService:
    def __init__(self, payment_method_repository: PaymentMethodRepository = Depends(),
                product_discount_repository: ProductDiscountRepository = Depends()):
        self.payment_method_repository = payment_method_repository
        self.product_discount_repository = product_discount_repository

    def create_discount(self, discount: ProductDiscountSchema):
        self.validator_discount(discount)
        self.product_discount_repository.create(ProductDiscount)

    def validator_discount(self, id: int, discount: ProductDiscountSchema):
        payment_method_query = self.payment_method_repository.get_by_id(discount.payment_method_id)
        if self.product_discount_repository.get_by_product_and_payment_method(discount.product_id, discount.payment_method_id):
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Payment method already discounted for this product')  
        elif payment_method_query.enabled != True:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Invalid payment method')
        elif discount.value == 0:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Invalid value')

    def update_discount(self, id: int, discount: ProductDiscountSchema):
        self.validator_discount_updated(id, discount)
        self.product_discount_repository.update(id, discount.dict())

    def validator_discount_updated(self, id: int, discount: ProductDiscountSchema):
        payment_method_query = self.payment_method_repository.get_by_id(discount.payment_method_id)
        discount_query = self.product_discount_repository.get_product_payment(discount.payment_method_id, discount.product_id)
        if discount_query and discount_query.id != id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Payment method already discounted for this product') 
        elif not payment_method_query or payment_method_query.enabled == False:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Invalid payment method')
        elif discount.value == 0:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Invalid value')
        