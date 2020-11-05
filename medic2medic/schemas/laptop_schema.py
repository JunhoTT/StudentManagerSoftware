from .. import ma
from ..models.laptop import LaptopModel

class LaptopSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = LaptopModel
