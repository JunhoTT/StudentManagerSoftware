from .. import ma
from ..models.student import StudentModel

class StudentSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = StudentModel
