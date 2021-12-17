from fastapi.exceptions import HTTPException
from fastapi.param_functions import Depends
from starlette import status
from app.repositories.payment_method_repository import PaymentMethodRepository
from app.repositories.product_discount_repository import ProductDiscountRepository
from app.repositories.product_repository import ProductRepository
from app.api.product_discount.schemas import ProductDiscountSchema
from app.models.models import PaymentMethods, Product, ProductDiscount

class ProductDiscountService:
    def __init__(self, payment_method_repository: PaymentMethodRepository = Depends(), product_discount_repository: ProductDiscountRepository = Depends(),
                 product_repository: ProductRepository = Depends()):
        self.payment_method_repository = payment_method_repository
        self.product_discount_repository = product_discount_repository
        self.product_repository = product_repository

    def create_discount( self, discount: ProductDiscountSchema):
        self.validate_discount(discount)
        self.product_discount_repository.create(ProductDiscount(**discount.dict()))

    def update_discount( self, id: int, discount: ProductDiscountSchema):
        self.validate_discount_update(id, discount)
        self.product_discount_repository.update(id, discount.dict())

    def validate_discount(self, discount: ProductDiscountSchema):
        payment_method_query = self.payment_method_repository.get_by_id(discount.payment_method_id)
        if self.product_discount_repository.get_by_product_and_payment_method(discount.product_id, discount.payment_method_id):
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Already discounted for this product')
        elif not self.product_repository.get_by_id(discount.product_id):
             raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Invalid product')            
        elif payment_method_query.enabled != True:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Invalid payment method')          
        elif discount.value == 0:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Invalid value')

    def validate_discount_update(self, id:int, discount: ProductDiscountSchema):
        payment_method_query = self.payment_method_repository.get_by_id(discount.payment_method_id)
        query_discount = self.product_discount_repository.get_by_product_and_payment_method(discount.product_id, discount.payment_method_id)
        if query_discount and query_discount.id != id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Already discounted for this product')         
        elif not self.product_repository.get_by_id(discount.product_id):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Invalid product')
        elif discount.value == 0:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Invalid value')
        elif not payment_method_query or payment_method_query.enabled == False:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Invalid payment method') 