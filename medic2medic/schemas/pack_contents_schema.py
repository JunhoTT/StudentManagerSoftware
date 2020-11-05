from .. import ma
from ..models.pack_content import PackContentModel

class PackContentSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = PackContentModel
