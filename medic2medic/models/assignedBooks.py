from .. import db


class AssignedBookModel(db.Model):
    """Data model for Books."""

    __tablename__ = 'assignedBooks'
    id = db.Column(
        db.Integer,
        primary_key=True
    )
    title = db.Column(
        db.String(80),
        index=True,
        nullable=False
    )
    studentid = db.Column(
        db.Integer,
        db.ForeignKey('students.id'),
        index=True
    )
    dategiven = db.Column(
        db.DateTime
    )



    def __repr__(self):
        return "<Uni (uni_name='%s')>" % (self.book_title)

