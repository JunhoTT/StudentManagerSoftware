from .. import db

class StudentPackContentsModel(db.Model):
    """Model for equipment packs."""

    __tablename__ = 'student_pack_contents'
    studentid = db.Column(
        db.Integer,
        db.ForeignKey('students.id'),
        primary_key=True
    )
    packcontents = db.Column(
        db.Text,
        primary_key=True
    )
