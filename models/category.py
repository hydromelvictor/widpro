from .base import Base


class Category(Base):
    """
    Category model
    =================
    This class is a model for category collection in the database

    Args:
    -----
        - name: str
            name of the category
        - attributes: list
            list of attributes for the category
            each attribute is a dict with the following
    """

    def attributesFieldsChecker(self, *args) -> bool:

        for attr in args:
            if not isinstance(attr, dict):
                raise ValueError(
                    'Attributes must be a list of dictionaries'
                )

            if 'name' not in attr:
                raise ValueError('Name is required for each attribute')

            if 'type' not in attr:
                raise ValueError('Type is required for each attribute')

            if attr['type'] not in ['string', 'number', 'boolean']:
                raise ValueError(
                    'Type must be one of string, number, boolean')

            if 'required' not in attr:
                raise ValueError(
                    'Required flag is required for each attribute')

            if not isinstance(attr['required'], bool):
                raise ValueError('Required must be a boolean')

            if attr['required'] and 'default' not in attr:
                raise ValueError(
                    'value is required for required attributes')

            if 'default' in attr:
                if attr['type'] == 'string' and\
                        not isinstance(attr['default'], str):
                    raise ValueError(
                        'Default must be a string for string type')

                elif attr['type'] == 'number' and\
                        not isinstance(attr['default'], (int, float)):
                    raise ValueError(
                        'Default must be a number for number type')

                elif attr['type'] == 'boolean' and\
                        not isinstance(attr['default'], bool):
                    raise ValueError(
                        'Default must be a boolean for boolean type')

            if 'enum' in attr:
                if not isinstance(attr['enum'], list):
                    raise ValueError('Enum must be a list')

                if not all(
                        isinstance(
                            v,
                            {
                                'string': str,
                                'number': (int, float),
                                'boolean': bool
                            }[attr['type']]
                        ) for v in attr['enum']):
                    raise ValueError(f'All enum values must match the\
                            attribute type {attr["type"]}')

            if 'min' in attr and not isinstance(attr['min'], (int, float)):
                raise ValueError('Min must be a number')

            if 'max' in attr and not isinstance(attr['max'], (int, float)):
                raise ValueError('Max must be a number')

            if 'minlength' in attr and\
                    not isinstance(attr['minlength'], int):
                raise ValueError('Minlength must be an integer')

            if 'maxlength' in attr and\
                    not isinstance(attr['maxlength'], int):
                raise ValueError('Maxlength must be an integer')

        return True

    def fieldsChecker(self, **kwargs) -> bool:

        if not kwargs.get('name'):
            raise ValueError('Name is required for validation')

        if 'name' in kwargs and not isinstance(kwargs['name'], str):
            raise ValueError('Name must be a string')

        return True

    def create(self, **kwargs) -> str:
        if self.get(name=kwargs['name']) is None:
            raise ValueError('Category already exists')

        kwargs['attributes'] = []
        return super().create(**kwargs)

    def update(self, id: str, **kwargs) -> bool:
        res = self.get(id=id)
        if not res:
            raise ValueError('Category not found')
        if 'name' in kwargs:
            if self.get(kwargs['name']):
                raise ValueError('Category already exists')

        kwargs |= {k: v for k, v in res.items() if k not in kwargs.keys()}
        return super().update(id, **kwargs)

    def delete(self, id, **kwargs):
        res = self.get(id)
        if not res:
            raise ValueError('Category not found')

        from .product import Product

        if Product.count(category=id) > 0:
            raise ValueError('Category has products')

        return super().delete(id, **kwargs)

    def addAttributes(self, id: str, **kwargs) -> bool:
        res = self.get(id)
        if not res:
            raise ValueError('Category not found')

        if not self.attributesFieldsChecker(*[kwargs]):
            raise AttributeError('data invalid !!!')

        # verifier si l'attribut existe deja avec le meme nom
        if any(attr['name'] == kwargs['name'] for attr in res['attributes']):
            raise ValueError('Attribute already exists')

        try:
            res = self.collection.update_one(
                {'_id': id},
                {
                    '$push': {
                        'attributes': kwargs
                    }
                }
            )
            return res.modified_count > 0
        except Exception as e:
            raise ValueError(e)

    def updateAttributes(self, id: str, name: str, **kwargs) -> bool:
        # Récupérer le document correspondant
        res = self.get(id)
        if not res:
            raise ValueError('Category not found')

        # Trouver l'attribut avec le nom donné
        attribute = next(
            (attr for attr in res['attributes'] if attr['name'] == name), None)

        if not attribute:
            return False

        # Fusionner les nouvelles données avec les anciennes
        updated_attribute = {**attribute, **kwargs}

        # Vérifier la validité des champs
        if not self.attributesFieldsChecker(updated_attribute):
            raise AttributeError('Data invalid!')

        # Construire l'opération de mise à jour MongoDB
        try:
            update_query = {
                '$set': {
                    'attributes.$': updated_attribute
                }
            }
            res = self.collection.update_one(
                # Critère de recherche
                {'_id': id, 'attributes.name': name},
                update_query
            )
            return res.modified_count > 0
        except Exception as e:
            raise ValueError(f"Error updating attributes: {e}")

    def deleteAttrs(self, id: str, name: str) -> bool:
        res = self.get(id)
        if not res:
            raise ValueError('Category not found')

        if not any(attr['name'] == name for attr in res['attributes']):
            raise ValueError('Attribute not found')

        try:
            res = self.collection.update_one(
                {'_id': id},
                {
                    '$pull': {
                        'attributes': {
                            'name': name
                        }
                    }
                }
            )
            return res.modified_count > 0
        except Exception as e:
            raise ValueError(e)


Category = Category(index=['name'])
