from .. import db

class LaptopModel(db.Model):
    """Data model for laptops."""

    __tablename__ = 'laptops'
    id = db.Column(
        db.Integer,
        primary_key=True
    )
    studentid = db.Column(
        db.Integer,
        db.ForeignKey('students.id'),
        index=True
    )
    description = db.Column(
        db.Text,
        index=True
    )
    dategiven = db.Column(
        db.DateTime
    )
    comment = db.Column(
        db.Text
    )
