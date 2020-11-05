from flask import request, Response, current_app as app
from .. import db
from ..models.assignedBooks import AssignedBookModel
from ..schemas.assignedBook_schema import AssignedBookSchema
import datetime
from google_auth import CheckLogin

assignedBook_schema = AssignedBookSchema()
assignedBooks_schema = AssignedBookSchema(many=True)

@app.route('/assignedBooks/')
@CheckLogin()
def assignedBook_list():
    all_laptops = AssignedBookModel.query.all()
    return assignedBooks_schema.jsonify(all_laptops)

@app.route('/assignedBooks/<number>', methods=['GET'])
@CheckLogin()
def get_assignedBook(number):
    assignedBooks = AssignedBookModel.query.filter(AssignedBookModel.id == number).all()
    if not assignedBooks:
        return Response(status=404, response='No laptop found with the given id number.')
    return assignedBook_schema.jsonify(assignedBooks[0])

@app.route('/assignedBooks/<number>', methods=['PATCH'])
@CheckLogin()
def update_assignedBook(number):
    assignedBooks = AssignedBookModel.query.filter(AssignedBookModel.id == number).all()
    if not assignedBooks:
        return Response(status=404, response='No laptop found with the given id number.')
    assignedBook = assignedBooks[0]
    assignedBook.studentid = request.json.get('studentid', assignedBook.studentid)
    assignedBook.title = request.json.get('title', assignedBook.title)
    try:
        assignedBook.dategiven = datetime.datetime.strptime(request.json.get('dategiven'), '%Y-%m-%d')
    except:
        assignedBook.dategiven = None

    db.session.commit()
    return assignedBook_schema.jsonify(assignedBook)

@app.route('/assignedBooks', methods=['POST'])
@CheckLogin()
def create_assignedBook():
    assignedBook = AssignedBookModel(
        id = request.json.get('id'),
        studentid = request.json.get('studentid'),
        title = request.json.get('title', ''),
    )
    try:
        assignedBook.dategiven = datetime.datetime.strptime(request.json.get('dategiven'), '%Y-%m-%d')
    except:
        assignedBook.dategiven = None
    db.session.add(assignedBook)
    db.session.commit()
    return assignedBook_schema.jsonify(assignedBook)

@app.route('/assignedBooks/<number>', methods=['DELETE'])
@CheckLogin()
def delete_assignedBook(number):
    assignedBooks = AssignedBookModel.query.filter(AssignedBookModel.id == number).all()
    if not assignedBooks:
        return Response(status=404, response='No laptop found with the given id number.')
    db.session.delete(assignedBooks[0])
    db.session.commit()
    return assignedBook_schema.jsonify(assignedBooks[0])

@app.route('/student/<number>/assignedBooks')
@CheckLogin()
def list_assignedBooks_by_student(number):
    assignedBook = AssignedBookModel.query.filter(AssignedBookModel.studentid == number).all()
    return assignedBooks_schema.jsonify(assignedBook)
