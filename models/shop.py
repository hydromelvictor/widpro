from .base import Base


class Shop(Base):

    """
    Shop model
    =================
    This class is a model for shop collection in the database

    products: list of product
    price: decimal
    fee: decimal
    total: decimal
    customer: dict
        name: str
        email: str
        phone: str
        address: str
        city: str
        country: str
        card: dict
            number: str
            exp: str
            cvv: str
    """

    def fieldsChecker(self, **kwargs) -> bool:

        assert kwargs.get('products', []), 'products is required'
        assert kwargs.get('price', False), 'price is required'
        assert kwargs.get('fee', False), 'fee is required'
        assert kwargs.get('total', False), 'total is required'
        assert kwargs.get('customer', {}), 'customer is required'
        assert kwargs.get(
            'customer', {}).get('name', False), 'name is required'
        assert kwargs.get(
            'customer', {}).get('email', False), 'email is required'
        assert kwargs.get(
            'customer', {}).get('phone', False), 'phone is required'
        assert kwargs.get(
            'customer', {}).get('address', False), 'address is required'
        assert kwargs.get(
            'customer', {}).get('city', False), 'city is required'
        assert kwargs.get(
            'customer', {}).get('country', False), 'country is required'
        assert kwargs.get(
            'customer', {}).get('card', {}), 'card is required'
        assert kwargs.get(
            'customer', {}
            ).get('card', {}).get('number', False), 'number is required'
        assert kwargs.get(
            'customer', {}
            ).get('card', {}).get('exp', False), 'exp is required'
        assert kwargs.get(
            'customer', {}
            ).get('card', {}).get('cvv', False), 'cvv is required'

        return all(
            [
                kwargs.get('products', []),
                kwargs.get('price', False),
                kwargs.get('fee', False),
                kwargs.get('total', False),
                kwargs.get('customer', {}),
                kwargs.get('customer', {}).get('name', False),
                kwargs.get('customer', {}).get('email', False),
                kwargs.get('customer', {}).get('phone', False),
                kwargs.get('customer', {}).get('address', False),
                kwargs.get('customer', {}).get('city', False),
                kwargs.get('customer', {}).get('country', False),
                kwargs.get('customer', {}).get('card', {}),
                kwargs.get(
                    'customer', {}).get('card', {}).get('number', False),
                kwargs.get('customer', {}).get('card', {}).get('exp', False),
                kwargs.get('customer', {}).get('card', {}).get('cvv', False)
            ]
        )
