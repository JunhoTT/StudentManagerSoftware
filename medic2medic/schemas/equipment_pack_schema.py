from .. import ma
from ..models.equipment_pack import EquipmentPackModel

class EquipmentPackSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = EquipmentPackModel
