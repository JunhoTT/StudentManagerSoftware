from .. import ma
from ..models.tuition import TuitionModel

class TuitionSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = TuitionModel
