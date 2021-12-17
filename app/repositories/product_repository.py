from sqlalchemy.orm import Session
from fastapi import Depends
from app.repositories.base_repository import BaseRepository
from app.db.db import get_db
from app.models.models import Product, Category, ProductDiscount
from sqlalchemy.orm import Session, joinedload
from app.api.catalog.schemas import CatalogFilter
from fastapi_pagination.ext.sqlalchemy import paginate

class ProductRepository(BaseRepository):
    def __init__(self, session: Session = Depends(get_db)) -> None:
        super().__init__(session, Product)


    def get_for_catalog(self, filter: CatalogFilter):
        query = self.query()
        queryset = [
            Product.visible == True
        ]
        if filter.category_name:
            queryset.append(Category.name == filter.category_name)
        if filter.category_id:
            queryset.append(Product.category_id == filter.category_id)
        if filter.supplier_id:
            queryset.append(Product.supplier_id == filter.supplier_id)
        if filter.min_price:
            queryset.append(Product.price >= filter.min_price)
        if filter.max_price:
            queryset.append(Product.price <= filter.max_price)
        if filter.description:
            queryset.append(Product.description.like(
                f'%{filter.description}%'))

        query = query.filter(*queryset).options(joinedload(Product.category),
                                                joinedload(Product.supplier), joinedload(Product.discounts).subqueryload(ProductDiscount.payment_method))

        return paginate(query)