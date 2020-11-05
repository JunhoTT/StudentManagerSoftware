from .. import db


class UniModel(db.Model):
    """Data model for Universities."""

    __tablename__ = 'universities'
    id = db.Column(
        db.Integer,
        primary_key=True
    )
    uni_name = db.Column(
        db.String(80),
        index=True,
        # unique=True,
        nullable=False
    )
    country = db.Column(
        db.String(80),
        index=True,
        unique=False,
        nullable=False
    )


    def __repr__(self):
        return "<Uni (uni_name='%s')>" % (self.uni_name)

