from .base import Base


class Category(Base):
    """
    Category model
    =================
    This class is a model for category collection in the database

    """

    def fieldsChecker(self, **kwargs) -> bool:
        """
        attributes: array of dict
            item: dict
                name: str
                type: str
                required: bool
                default: any
                enum: list
                min: int
                max: int
                minlength: int
                maxlength: int
        """
        return all(
            [
                kwargs.get('name', False),
                kwargs.get('attributes', [])
            ]
        )


Category = Category()
