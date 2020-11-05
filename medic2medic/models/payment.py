from .. import db

class PaymentModel(db.Model):
    """Data model for payments."""

    __tablename__ = 'payments'
    id = db.Column(
        db.Integer,
        primary_key=True
    )
    studentid = db.Column(
        db.Integer,
        db.ForeignKey('students.id')
    )
    semester = db.Column(
        db.Text
    )
    stationery = db.Column(
        db.Text
    )
    living = db.Column(
        db.Text
    )
    uniform = db.Column(
        db.Text
    )
    transport = db.Column(
        db.Text
    )
    totalpayment = db.Column(
        db.Text
    )
    totalmk = db.Column(
        db.Text
    )
    received = db.Column(
        db.Boolean
    )
    paymentdate = db.Column(
        db.DateTime
    )
    comment = db.Column(
        db.Text
    )
