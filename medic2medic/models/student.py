from .. import db


class StudentModel(db.Model):
    """Data model for students."""

    __tablename__ = 'students'
    id = db.Column(
        db.Integer,
        primary_key=True
    )
    number = db.Column(
        db.String(80),
        #db.Integer,
        #unique=True
    )
    email = db.Column(
        db.String(80),
        index=True,
        nullable=False
    )
    email2 = db.Column(
        db.String(80),
        index=True,
    )
    firstname = db.Column(
        db.String(80),
        index=True,
        nullable=False
    )
    surname = db.Column(
        db.String(80),
        index=True,
    )
    contactnumber = db.Column(
        db.String(80),
        index=True,
    )
    contactnumber2 = db.Column(
        db.String(80),
        index=True,
    )
    bank = db.Column(
        db.String(80),
        index=True,
    )
    servicecentre = db.Column(
        db.String(80),
    )
    account = db.Column(
        db.String(80),
    )
    swift = db.Column(
        db.String(80),
    )
    fdh = db.Column(
        db.String(80),
    )
    equipmentpack = db.Column(
        db.Text
    )
    updated = db.Column(
        db.DateTime,
    )
    lateupdated = db.Column(
        db.DateTime,
    )
    created = db.Column(
        db.DateTime,
        index=False,
        unique=False,
        nullable=False
    )

    scholarship = db.Column(
        db.String(80),
    )
    dateStarted = db.Column(
        db.String(80),
    )
    signed = db.Column(
        db.String(80),
    )
    sponsored = db.Column(
        db.String(80),
    )
    fees = db.Column(
        db.String(80),
    )
    upkeep = db.Column(
        db.String(80),
    )
    course = db.Column(
        db.String(80),
        index=True,
        unique=False
    )
    country = db.Column(
        db.String(80),
        index=True,
        unique=False
    )
    university = db.Column(
        db.String(80),
        index=True,
        unique=False
    )
    currentacademicyear = db.Column(
        db.String(80),
        index=True,
        unique=False
    )
    mentor = db.Column(
        db.String(80),
        index=True,
        unique=False
    )
    mentormatchdate = db.Column(
        db.String(80),
        index=True,
        unique=False
    )
    status = db.Column(
        db.String(80),
        index=True,
        unique=False
    )


    def __repr__(self):
        return "<Student (firstname='%s', surname='%s')>" % (self.firstname, self.surname)

