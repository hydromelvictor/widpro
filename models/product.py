from .base import Base
from decimal import Decimal
import typing


class Product(Base):

    """
    Product model
    =================
    This class is a model for product collection in the database

    """

    def fieldsChecker(self, **kwargs: dict[str, typing.Any]) -> bool:
        """
        Validates the fields provided in kwargs for creating or
        updating an entity.

        :raises ValueError: If any required field is missing or has
        incorrect type.
        :return: True if all validations pass.
        """
        if not kwargs.get('author'):
            raise ValueError("Field 'author' is required")

        if not kwargs.get('name'):
            raise ValueError("Field 'name' is required")

        assert isinstance(kwargs.get('name'), str), \
            "Field 'name' must be a string"

        if not kwargs.get('description'):
            kwargs['description'] = 'No description'

        price = kwargs.get('price')
        if price is None or not isinstance(price, Decimal):
            raise ValueError("Field 'price' must be of type Decimal")

        stock = kwargs.get('stock', 1)
        if not isinstance(stock, int):
            try:
                stock = int(stock)
            except ValueError:
                raise ValueError("Field 'stock' must be an integer")

        if not kwargs.get('category'):
            raise ValueError("Field 'category' is required")

        from .category import Category
        if not Category.get(id=kwargs.get('category')):
            raise ValueError("Category does not exist")

        if not kwargs.get('image'):
            raise ValueError("Field 'image' is required")

        if not kwargs.get('status'):
            kwargs['status'] = 'available'

        # If we reach here without raising an exception,
        # all validations have passed
        return True


Product = Product()
