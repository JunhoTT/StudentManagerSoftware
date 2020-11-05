from .. import ma
from ..models.payment import PaymentModel

class PaymentSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = PaymentModel
