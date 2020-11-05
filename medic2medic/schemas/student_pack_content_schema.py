from .. import ma
from ..models.student_pack_content import StudentPackContentModel

class StudentPackContentSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = StudentPackContentModel
