from flask import request, render_template, make_response, jsonify, redirect
from datetime import datetime as dt
from flask import current_app as app
#from .student import db, User
from ..schemas.student_schema import StudentSchema
from ..models.student import StudentModel
from .. import db
from google_auth import CheckLogin
import os

student_schema = StudentSchema()
students_schema = StudentSchema(many=True)

@app.route('/student/')
@CheckLogin()
def student_list():
    all_students = StudentModel.query.all()
    return jsonify(students_schema.dump(all_students))

@app.route('/student/<number>')
@CheckLogin()
def student_by_number(number):
    #students = StudentModel.query.filter(StudentModel.number == number).all()
    students = StudentModel.query.filter(StudentModel.id == number).all()
    return jsonify(student_schema.dump(students[0]))

@app.route('/student/<number>/dates', methods=['PATCH'])
@CheckLogin()
def update_student_dates(number):
    #student = StudentModel.query.filter(StudentModel.number == number).all()[0]
    student = StudentModel.query.filter(StudentModel.id == number).all()[0]
    student.updated = dt.strptime(request.json.get('updated'), '%Y-%m-%d')
    student.lateupdated = dt.strptime(request.json.get('lateupdated'), '%Y-%m-%d')
    db.session.commit()
    return jsonify(student_schema.dump(student))

@app.route('/student/', methods=['POST'])
@CheckLogin()
def create_student():
    firstname = request.json.get('firstname', '')
    surname = request.json.get('surname', '')
    email = request.json.get('email', '')
    contactnumber = request.json.get('contactnumber', '')
    number = request.json.get('number', '')
    status = request.json.get('status', '')
    student = StudentModel(
        firstname=firstname,
        surname=surname,
        email=email,
        number=number,
        contactnumber=contactnumber,
        status=status,
        created = dt.now()
    )
    db.session.add(student)
    db.session.commit()
    return student_schema.jsonify(student)

@app.route('/student/', methods=['PATCH'])
@CheckLogin()
def update_student():
    id = request.json.get('id', '')#
    email = request.json.get('email', '')
    email2 = request.json.get('email2', '')
    firstname = request.json.get('firstname', '')
    surname = request.json.get('surname', '')
    contactnumber = request.json.get('contactnumber', '')
    contactnumber2 = request.json.get('contactnumber2', '')
    number = request.json.get('number', '')
    status = request.json.get('status', '')

    bank = request.json.get('bank', '')
    servicecentre = request.json.get('servicecentre', '')
    account = request.json.get('account', '')
    swift = request.json.get('swift', '')
    fdh = request.json.get('fdh', '')
    
    scholarship = request.json.get('scholarship', '')
    dateStarted = request.json.get('dateStarted', '')
    signed = request.json.get('signed', '')
    sponsored = request.json.get('sponsored', '')
    fees = request.json.get('fees', '')
    upkeep = request.json.get('upkeep', '')

    course = request.json.get('course', '')
    enrolmentid = request.json.get('enrolmentid', '')
    country = request.json.get('country', '')
    university = request.json.get('university', '')
    currentacademicyear = request.json.get('currentacademicyear', '')
    mentor = request.json.get('mentor', '')
    mentormatchdate = request.json.get('mentormatchdate', '')

    #students = StudentModel.query.filter(StudentModel.number == number).all()
    students = StudentModel.query.filter(StudentModel.id == id).all()#
    student = students[0]
    student.email = email
    student.email2 = email2
    student.firstname = firstname
    student.surname = surname
    student.contactnumber = contactnumber
    student.contactnumber2 = contactnumber2
    student.number = number #
    student.status = status

    student.bank = bank
    student.servicecentre = servicecentre
    student.account = account
    student.swift = swift
    student.fdh = fdh
    
    student.scholarship = scholarship
    student.dateStarted = dateStarted
    student.signed = signed
    student.sponsored = sponsored
    student.fees = fees
    student.upkeep = upkeep

    student.enrolmentid = enrolmentid
    student.course = course
    student.university = university
    student.currentacademicyear = currentacademicyear
    student.country = country
    student.mentor = mentor
    student.mentormatchdate = mentormatchdate

    db.session.commit()
    return student_schema.jsonify(student)

@app.route('/student/<id>', methods=['DELETE'])
def delete_student(id):
    StudentModel.query.filter_by(id=id).delete()
    db.session.commit()
    all_students = StudentModel.query.all()
    return jsonify(students_schema.dump(all_students))

@app.route('/list/students')
@CheckLogin(redirect=True)
def list_students():
    return render_template('student_list.html')

@app.route('/edit/student/<number>')
@CheckLogin(redirect=True)
def edit_student(number):
    students = StudentModel.query.filter(StudentModel.id == number).all()
    if not students:
        return render_template('not_found.html')
    s3Bucket = os.environ.get('S3_BUCKET', '')
    return render_template('student.html', studentNumber=number, s3Bucket=s3Bucket)
