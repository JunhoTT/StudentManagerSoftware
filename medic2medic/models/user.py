from .. import db
from datetime import datetime as dt
import os

class UserModel(db.Model):
    """Data model for user accounts."""

    __tablename__ = 'users'
    id = db.Column(
        db.Integer,
        primary_key=True
    )
    email = db.Column(
        db.String(80),
        index=True,
        unique=True,
        nullable=False
    )
    permissions = db.Column(
        db.String(80),
        index=True,
        nullable=False
    )

    def __repr__(self):
        return '<User {}>'.format(self.email)

def setup_admin():
    ADMIN_EMAIL = os.environ.get("ADMIN_EMAIL", default=False)
    if ADMIN_EMAIL:
        users = UserModel.query.filter(UserModel.email == ADMIN_EMAIL).all()
        if users:
            users[0].permissions = str(['read', 'write', 'admin'])
        else:
            admin_user = UserModel(
                email=ADMIN_EMAIL,
                permissions=str(['read', 'write', 'admin'])
            )
            db.session.add(admin_user)
        db.session.commit()

def log_admins():
    import logging
    admins = UserModel.query.all()
    admins = [ admin for admin in admins if 'admin' in eval(admin.permissions) ]
    logging.info("Admin users:")
    for admin in admins:
        logging.info(f"\t{admin}")

