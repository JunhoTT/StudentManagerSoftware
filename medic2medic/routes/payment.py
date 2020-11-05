from flask import request, Response, current_app as app
from .. import db
from ..models.payment import PaymentModel
from ..schemas.payment_schema import PaymentSchema
from google_auth import CheckLogin
import datetime

payment_schema = PaymentSchema()
payments_schema = PaymentSchema(many=True)

@app.route('/payment/')
@CheckLogin()
def payment_list():
    all_payments = PaymentModel.query.all()
    return payments_schema.jsonify(all_payments)

@app.route('/payment/<number>', methods=['GET'])
@CheckLogin()
def get_payment(number):
    payments = PaymentModel.query.filter(PaymentModel.id == number).all()
    if not payments:
        return Response(status=404, response='No payment found with the given id number.')
    return payment_schema.jsonify(payments[0])

@app.route('/payment/<number>', methods=['PATCH'])
@CheckLogin()
def update_payment(number):
    payments = PaymentModel.query.filter(PaymentModel.id == number).all()
    if not payments:
        return Response(status=404, response='No payment found with the given id number.')
    payment = payments[0]
    payment.studentid = request.json.get('studentid', payment.studentid)
    payment.semester = request.json.get('semester', payment.semester)
    payment.stationery = request.json.get('stationery', payment.stationery)
    payment.living = request.json.get('living', payment.living)
    payment.uniform = request.json.get('uniform', payment.uniform)
    payment.transport = request.json.get('transport', payment.transport)
    payment.totalpayment = request.json.get('totalpayment', payment.totalpayment)
    payment.totalmk = request.json.get('totalmk', payment.totalmk)
    payment.received = request.json.get('received', payment.received)
    try:
        payment.paymentdate = datetime.datetime.strptime(request.json.get('paymentdate'), '%Y-%m-%d')
    except:
        payment.paymentdate = None
    payment.comment = request.json.get('comment', payment.comment)
    db.session.commit()
    return payment_schema.jsonify(payment)

@app.route('/payment', methods=['POST'])
@CheckLogin()
def create_payment():
    payment = PaymentModel(
        id = request.json.get('id'),
        studentid = request.json.get('studentid'),
        semester = request.json.get('semester', ''),
        stationery = request.json.get('stationery', ''),
        living = request.json.get('living', ''),
        uniform = request.json.get('uniform', ''),
        transport = request.json.get('transport', ''),
        totalpayment = request.json.get('totalpayment', ''),
        totalmk = request.json.get('totalmk', ''),
        received = request.json.get('received', False),
        comment = request.json.get('comment', '')
    )
    try:
        payment.paymentdate = datetime.datetime.strptime(request.json.get('paymentdate'), '%Y-%m-%d')
    except:
        payment.paymentdate = None
    db.session.add(payment)
    db.session.commit()
    return payment_schema.jsonify(payment)

@app.route('/payment/<number>', methods=['DELETE'])
@CheckLogin()
def delete_payment(number):
    payments = PaymentModel.query.filter(PaymentModel.id == number).all()
    if not payments:
        return Response(status=404, response='No payment found with the given id number.')
    db.session.delete(payments[0])
    db.session.commit()
    return payment_schema.jsonify(payments[0])

@app.route('/student/<number>/payments')
@CheckLogin()
def list_payments_by_student(number):
    payments = PaymentModel.query.filter(PaymentModel.studentid == number).all()
    return payments_schema.jsonify(payments)
