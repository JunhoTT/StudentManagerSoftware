from .. import db


class BookModel(db.Model):
    """Data model for Books."""

    __tablename__ = 'books'
    id = db.Column(
        db.Integer,
        primary_key=True
    )
    title = db.Column(
        db.String(80),
        index=True,
        nullable=False
    )
    author = db.Column(
        db.String(80),
        index=True,
        nullable=False
    )




    def __repr__(self):
        return "<Uni (uni_name='%s')>" % (self.book_title)

