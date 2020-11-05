from flask import request, render_template, make_response, jsonify
from datetime import datetime as dt
from flask import current_app as app
#from .student import db, User
from ..schemas.student_schema import StudentSchema
from ..models.student import StudentModel
from ..schemas.laptop_schema import LaptopSchema
from ..models.laptop import LaptopModel
from ..schemas.assignedBook_schema import AssignedBookSchema
from ..models.assignedBooks import AssignedBookModel
from ..schemas.payment_schema import PaymentSchema
from ..models.payment import PaymentModel
from ..schemas.tuition_schema import TuitionSchema
from ..models.tuition import TuitionModel
from .. import db
from google_auth import CheckLogin

student_schema = StudentSchema()
students_schema = StudentSchema(many=True)

laptop_schema = LaptopSchema()
laptops_schema = LaptopSchema(many=True)

assignedBook_schema = AssignedBookSchema()
assignedBooks_schema = AssignedBookSchema(many=True)

payment_schema = PaymentSchema()
payments_schema = PaymentSchema(many=True)

tuition_schema = TuitionSchema()
tuitions_schema = TuitionSchema(many=True)

@app.route('/reports/contact')
@CheckLogin()
def report_student_contact_details():
    all_students = StudentModel.query.order_by(StudentModel.university.asc(), StudentModel.course.asc(), StudentModel.surname.asc()).all()
    return jsonify(students_schema.dump(all_students))

@app.route('/reports/nocontract')
@CheckLogin()
def report_student_no_contract():
    all_students = StudentModel.query.filter(StudentModel.signed == "tosign").order_by(StudentModel.university.asc(), StudentModel.course.asc(), StudentModel.surname.asc()).all()
    return jsonify(students_schema.dump(all_students))

@app.route('/reports/updatedate')
@CheckLogin()
def report_student_by_updatedate():
    all_students = StudentModel.query.filter(StudentModel.lateupdated != None).order_by(StudentModel.lateupdated.desc()).all()
    return jsonify(students_schema.dump(all_students))

@app.route('/reports/noprofile')
@CheckLogin()
def report_student_no_profile():
    all_students = StudentModel.query.filter(StudentModel.updated == None).order_by(StudentModel.university.asc(), StudentModel.course.asc(), StudentModel.surname.asc()).all()
    return jsonify(students_schema.dump(all_students))

@app.route('/reports/mentor')
@CheckLogin()
def report_student_by_mentor():
    all_students = StudentModel.query.filter(StudentModel.mentor != None).order_by(StudentModel.university.asc(), StudentModel.course.asc(), StudentModel.surname.asc()).all()
    return jsonify(students_schema.dump(all_students))

@app.route('/reports/nomentor')
@CheckLogin()
def report_student_no_mentor():
    all_students = StudentModel.query.filter(StudentModel.mentor == None).order_by(StudentModel.university.asc(), StudentModel.course.asc(), StudentModel.surname.asc()).all()
    return jsonify(students_schema.dump(all_students))

@app.route('/reports/laptop')
@CheckLogin()
def report_student_by_laptop():
    all_laptops = LaptopModel.query.join(StudentModel, LaptopModel.studentid == StudentModel.id).add_columns(StudentModel.id, LaptopModel.description, LaptopModel.dategiven, LaptopModel.comment).all()
    return laptops_schema.jsonify(all_laptops)

@app.route('/reports/nolaptop')
@CheckLogin()
def report_student_no_laptop():
    all_students = StudentModel.query.outerjoin(LaptopModel, StudentModel.id == LaptopModel.studentid).filter(LaptopModel.studentid == None).order_by(StudentModel.university.asc(), StudentModel.course.asc(), StudentModel.surname.asc()).all()
    return students_schema.jsonify(all_students)

@app.route('/reports/pack')
@CheckLogin()
def report_student_pack():
    all_students = StudentModel.query.filter(StudentModel.equipmentpack != None).order_by(StudentModel.university.asc(), StudentModel.course.asc(), StudentModel.surname.asc()).all()
    return jsonify(students_schema.dump(all_students))

@app.route('/reports/nopack')
@CheckLogin()
def report_student_no_pack():
    all_students = StudentModel.query.filter(StudentModel.equipmentpack == None).order_by(StudentModel.university.asc(), StudentModel.course.asc(), StudentModel.surname.asc()).all()
    return jsonify(students_schema.dump(all_students))

@app.route('/reports/nobook')
@CheckLogin()
def report_student_no_book():
    all_students = StudentModel.query.outerjoin(AssignedBookModel, StudentModel.id == AssignedBookModel.studentid).filter(AssignedBookModel.studentid == None).order_by(StudentModel.university.asc(), StudentModel.course.asc(), StudentModel.surname.asc()).all()
    return students_schema.jsonify(all_students)

@app.route('/reports/payment')
@CheckLogin()
def report_payment():
    all_payments = PaymentModel.query.join(StudentModel, PaymentModel.studentid == StudentModel.id).add_columns(StudentModel.id, PaymentModel.semester, PaymentModel.totalpayment, PaymentModel.totalmk, PaymentModel.received, PaymentModel.paymentdate).order_by(PaymentModel.paymentdate.desc()).all()
    return payments_schema.jsonify(all_payments)

@app.route('/reports/nopayment')
@CheckLogin()
def report_no_payment():
    all_payments = PaymentModel.query.join(StudentModel, PaymentModel.studentid == StudentModel.id).add_columns(StudentModel.id, PaymentModel.semester, PaymentModel.totalpayment, PaymentModel.totalmk, PaymentModel.received, PaymentModel.paymentdate).filter(PaymentModel.received == False).all()
    return payments_schema.jsonify(all_payments)

@app.route('/reports/tuition')
@CheckLogin()
def report_tuition():
    all_tuitions = TuitionModel.query.join(StudentModel, TuitionModel.studentid == StudentModel.id).add_columns(StudentModel.id, TuitionModel.year, TuitionModel.feestructure, TuitionModel.partialscholarship, TuitionModel.feebalance, TuitionModel.feepaid).all()
    return tuitions_schema.jsonify(all_tuitions)


@app.route('/reports/')
@CheckLogin(redirect=True)
def report_list_students():
    return render_template('reports.html')
