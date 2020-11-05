from .. import db

class EquipmentPackContentModel(db.Model):
    """Model for equipment packs."""

    __tablename__ = 'equipment_pack_contents'
    # __table_args__ = (
    #     db.PrimaryKeyConstraint('equipmentpack', 'packcontents'),
    # )
    equipmentpack = db.Column(
        db.Text,
        db.ForeignKey('equipment_packs.packname'),
        primary_key=True
    )
    packcontents = db.Column(
        db.Text,
        primary_key=True
    )
