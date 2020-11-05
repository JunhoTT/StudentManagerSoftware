from .. import ma
from ..models.book import BookModel

class BookSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = BookModel
