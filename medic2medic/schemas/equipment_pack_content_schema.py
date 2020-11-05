from .. import ma
from ..models.equipment_pack_content import EquipmentPackContentModel

class EquipmentPackContentSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = EquipmentPackContentModel
