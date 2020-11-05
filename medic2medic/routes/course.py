from flask import request, render_template, make_response, jsonify
from datetime import datetime as dt
from flask import current_app as app
#from .student import db, User
from ..schemas.course_schema import CourseSchema
from ..models.course import CourseModel
from .. import db
from google_auth import CheckLogin

course_schema = CourseSchema()
courses_schema = CourseSchema(many=True)
@app.route('/course/')
@CheckLogin()
def course_list():
    all_courses = CourseModel.query.all()
    return jsonify(courses_schema.dump(all_courses))

@app.route('/course/<number>')
@CheckLogin()
def course_by_number(number):
    courses = CourseModel.query.filter(CourseModel.id == number).all()
    return jsonify(course_schema.dump(courses[0]))


@app.route('/course/', methods=['POST'])
@CheckLogin()
def create_course():
    course_name = request.json.get('course_name', '')


    course = CourseModel(
        course_name=course_name

    )
    db.session.add(course)
    db.session.commit()
    return course_schema.jsonify(course)

@app.route('/course/', methods=['PATCH'])
@CheckLogin()
def update_course():
    course_name = request.json.get('course_name', '')
    id = request.json.get('id', '')

    courses = CourseModel.query.filter(CourseModel.id == id).all()

    course = courses[0]
    course.course_name = course_name

    db.session.commit()
    return course_schema.jsonify(course)

@app.route('/course/<id>', methods=['DELETE'])
def delete_course(id):
    CourseModel.query.filter_by(id=id).delete()
    db.session.commit()
    all_courses = CourseModel.query.all()
    return jsonify(courses_schema.dump(all_courses))

@app.route('/list/courses')
@CheckLogin(redirect=True)
def list_courses():
    return render_template('courses.html')

@app.route('/edit/course/<number>')
@CheckLogin(redirect=True)
def edit_course(number):
    courses = CourseModel.query.filter(CourseModel.id == number).all()
    if not courses:
        return render_template('not_found.html')
    return render_template('course.html', id=number)
