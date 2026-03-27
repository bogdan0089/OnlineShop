from schemas.schemas import ProductsCreate, ProductUpdate
from models.models import Product
from database.unit_of_work import UnitOfWork
from core.exceptions import ProductNotFound, ProductsNotFound

class ProductService:



    @staticmethod
    async def create_product(data: ProductsCreate) -> Product:
        async with UnitOfWork() as uow:
            return await uow.product.create_product(data)

    @staticmethod
    async def get_product(product_id: int) -> Product:
        async with UnitOfWork() as uow:
            products = await uow.product.get_product(product_id)
            if not products:
                raise ProductNotFound(product_id)
            return products
        

    @staticmethod
    async def get_products():
        async with UnitOfWork() as uow:
            products = await uow.product.get_products()
            if products is None:
                raise ProductsNotFound()
            return products
        
    @staticmethod
    async def update_product(product_id: int, data: ProductUpdate):
        async with UnitOfWork() as uow:
            product = await uow.product.get_product(product_id)
            if product is None:
                raise ProductNotFound(product_id)
            update_products = await uow.product.update_product(product, data)
            return update_products

    
    @staticmethod
    async def delete_product(product_id: int):
        async with UnitOfWork() as uow:
            product = await uow.product.get_product(product_id)
            if product is None:
                raise ProductNotFound(product_id)
            delete_product = await uow.product.delete_product(product)
            return delete_product

    @staticmethod
    async def search_products(name: str):
        async with UnitOfWork() as uow:
            products = await uow.product.search_by_name(name)
            if not products:
                raise ProductsNotFound()
            return products

    @staticmethod
    async def filter_by_price(min_price: float = None, max_price: float = None):
        async with UnitOfWork() as uow:
            products = await uow.product.filter_by_price(min_price, max_price)
            if not products:
                raise ProductsNotFound()
            return products

