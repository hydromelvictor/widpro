from .base import Base
from decimal import Decimal
import typing


data_type = {
    'string': str,
    'number': (int, float),
    'boolean': bool
}


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
        if 'author' not in kwargs:
            raise ValueError("Field 'author' is required")

        if 'name' not in kwargs:
            raise ValueError("Field 'name' is required")

        assert isinstance(kwargs.get('name'), str), \
            "Field 'name' must be a string"

        if 'description' not in kwargs:
            kwargs['description'] = 'No description'

        try:
            price = Decimal(kwargs.get('price'))
        except Exception as e:
            raise ValueError(str(e))

        if price is None or not isinstance(price, Decimal):
            raise ValueError("Field 'price' must be of type Decimal")

        stock = kwargs.get('stock', 1)
        if not isinstance(stock, int):
            try:
                stock = int(stock)
            except Exception as e:
                raise ValueError(str(e))

        if 'category' not in kwargs:
            raise ValueError("Field 'category' is required")

        from .category import Category
        if not Category.get(id=kwargs.get('category')):
            raise ValueError("Category does not exist")

        if 'image' not in kwargs:
            raise ValueError("Field 'image' is required")

        if 'status' not in kwargs:
            kwargs['status'] = 'available'

        from .category import Category

        id = kwargs['category']

        res = Category.get(id)
        if not res:
            raise ValueError('data not found')

        if len(res['attributes']) > 0:
            if not self.attrsChecker(id, **kwargs['attributes']):
                raise AttributeError('data invalid !!!')
            else:
                kwargs['attributes'] = {}

        # If we reach here without raising an exception,
        # all validations have passed
        return True

    def attrsChecker(self, id: str, **kwargs) -> bool:

        from .category import Category

        res = Category.get(id)
        if not res:
            raise ValueError('data not found')

        for attr in res['attributes']:
            if attr['name'] in kwargs:
                key = attr['name']
                value = kwargs.get(key)

                if attr['required'] and not value:
                    raise ValueError('value required')

                if value:
                    assert isinstance(
                        value, data_type[attr['type']]), 'error type'

                    enum = attr.get('enum')
                    if enum and value not in enum:
                        raise ValueError(f'value not in {enum}')

                    min = attr.get('min')
                    if min and value < min:
                        raise ValueError(f'value must be great or equal {min}')

                    max = attr.get('max')
                    if max and value > max:
                        raise ValueError(f'value must be less or equal {max}')

                    if type(value) is str:
                        minlength = attr.get('minlength')
                        if minlength and len(value) < minlength:
                            raise ValueError(
                                f'value must be great or equal {minlength}')

                        maxlength = attr.get('maxlength')
                        if maxlength and len(value) > maxlength:
                            raise ValueError(
                                f'value must be less or equal {maxlength}')
            else:
                raise AttributeError(f'{attr['name']} required')

        return True

    def update(self, id, **kwargs):
        res = self.get(id)
        if not res:
            raise ValueError('Product not found')

        update_attrs = {**res, **kwargs}
        return super().update(id, **update_attrs)


Product = Product()
