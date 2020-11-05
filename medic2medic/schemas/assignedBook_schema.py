from .. import ma
from ..models.assignedBooks import AssignedBookModel

class AssignedBookSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = AssignedBookModel
