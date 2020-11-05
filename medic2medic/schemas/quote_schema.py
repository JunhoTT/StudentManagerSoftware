from .. import ma
from ..models.quotes import QuoteModel

class QuoteSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = QuoteModel
