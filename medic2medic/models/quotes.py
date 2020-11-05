from .. import db

class QuoteModel(db.Model):
    """Data model for quoutes."""

    __tablename__ = 'quotes'
    id = db.Column(
        db.Integer,
        primary_key=True
    )
    studentid = db.Column(
        db.Integer,
        db.ForeignKey('students.id')
    )
    text = db.Column(
        db.Text
    )
