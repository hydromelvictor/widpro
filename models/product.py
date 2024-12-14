from .base import Base
from decimal import Decimal


class Product(Base):

    """
    Product model
    =================
    This class is a model for product collection in the database

    """

    def fieldsChecker(self, **kwargs) -> bool:

        assert kwargs.get('author', False), 'author is required'
        assert kwargs.get('name', False), 'name is required'
        assert kwargs.get(
            'description', 'No description'), 'description is required'
        assert kwargs.get(
            'price', False
            ) and type(kwargs.get('price')) == Decimal, 'price is required'
        assert kwargs.get(
            'stock', 1
            ) and type(kwargs.get('stock')) == int, 'stock is required'
        assert kwargs.get('category', False), 'category is required'
        assert kwargs.get('image', False), 'image is required'
        assert kwargs.get('status', 'available'), 'status is required'

        return all(
            [
                kwargs.get('author', False),
                kwargs.get('name', False),
                kwargs.get('description', 'No description'),
                kwargs.get('price', False),
                kwargs.get('stock', 1),
                kwargs.get('category', False),
                kwargs.get('image', False),
                kwargs.get('status', 'available'),
                kwargs.get('type', False)
            ]
        )


Product = Product()
