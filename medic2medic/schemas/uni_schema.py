from .. import ma
from ..models.university import UniModel

class UniSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = UniModel
