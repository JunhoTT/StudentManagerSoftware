from .. import db

class TuitionModel(db.Model):
    """Data model for tuition fees."""

    __tablename__ = 'tuition'
    id = db.Column(
        db.Integer,
        primary_key=True
    )
    studentid = db.Column(
        db.Integer,
        db.ForeignKey('students.id')
    )
    year = db.Column(
        db.Text
    )
    feestructure = db.Column(
        db.Text
    )
    partialscholarship = db.Column(
        db.Text
    )
    feebalance = db.Column(
        db.Text
    )
    feepaid = db.Column(
        db.Text
    )
