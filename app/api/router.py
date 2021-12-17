from fastapi import APIRouter
from .product.views import router as product_router
from .coupons.views import router as coupons_router
from .address.views import router as address_router
from .category.views import router as category_router
from .supplier.views import router as supplier_router 
from .payment_methods.views import router as payment_methods_router
from .product_discount.views import router as product_discount_router

from .customers.views import router as customer_router

router = APIRouter()

router.include_router(product_router, prefix='/products', tags=['product'])
router.include_router(supplier_router, prefix='/suppliers', tags=['supplier'])
router.include_router(category_router, prefix='/categories', tags=['category'])
router.include_router(payment_methods_router, prefix='/paymentmethods', tags=['payment-method'])
router.include_router(product_discount_router, prefix='/prodcuctdiscounts', tags=['product-discount'])
router.include_router(coupons_router, prefix='/coupons', tags=['coupons'])
router.include_router(customer_router, prefix='/customer', tags=['customer'])
router.include_router(address_router, prefix='/address', tags=['address'])
