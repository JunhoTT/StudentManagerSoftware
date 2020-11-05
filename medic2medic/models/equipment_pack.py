from .. import db

class EquipmentPackModel(db.Model):
    """Model for equipment packs."""

    __tablename__ = 'equipment_packs'
    packname = db.Column(
        db.Text,
        primary_key=True
    )
