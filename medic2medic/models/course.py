from .. import db


class CourseModel(db.Model):
    """Data model for Courses."""

    __tablename__ = 'courses'
    id = db.Column(
        db.Integer,
        primary_key=True
    )
    course_name = db.Column(
        db.String(80),
        index=True,
        unique=True,
        nullable=False
    )



    def __repr__(self):
        return "<Course (course_name='%s')>" % (self.course_name)

