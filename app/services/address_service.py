from fastapi.param_functions import Depends
from app.api.repositories.adress_repository import AddressRepository
from app.api.repositories.custumer_repository import CustomerRepository
from app.api.adress.schemas import AddressSchema
from fastapi import HTTPException, status

from app.models.models import Address

class AddressService:
    def __init__(self, address_repository: AddressRepository = Depends(), customer_repository: CustomerRepository = Depends()) -> None:
        self.address_repository = address_repository
        self.customer_repository = customer_repository

    def create(self, address: AddressSchema):
        if not self.customers_repository.get_by_id(address.customer_id):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Invalid customer')
        if address.primary:
            self.addresses_repository.remove_primary()
        self.addresses_repository.create(Address(**address.dict()))


    def update(self,id: int, address: AddressSchema):
        if not self.customers_repository.get_by_id(address.customer_id):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Invalid customer')
        if address.primary:
            self.addresses_repository.remove_primary()
        self.addresses_repository.update(id, address.dict())