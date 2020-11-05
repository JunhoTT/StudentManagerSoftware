from flask import request, Response, current_app as app
from .. import db
from ..models.laptop import LaptopModel
from ..schemas.laptop_schema import LaptopSchema
import datetime
from google_auth import CheckLogin

laptop_schema = LaptopSchema()
laptops_schema = LaptopSchema(many=True)

@app.route('/laptop/')
@CheckLogin()
def laptop_list():
    all_laptops = LaptopModel.query.all()
    return laptops_schema.jsonify(all_laptops)

@app.route('/laptop/<number>', methods=['GET'])
@CheckLogin()
def get_laptop(number):
    laptops = LaptopModel.query.filter(LaptopModel.id == number).all()
    if not laptops:
        return Response(status=404, response='No laptop found with the given id number.')
    return laptop_schema.jsonify(laptops[0])

@app.route('/laptop/<number>', methods=['PATCH'])
@CheckLogin()
def update_laptop(number):
    laptops = LaptopModel.query.filter(LaptopModel.id == number).all()
    if not laptops:
        return Response(status=404, response='No laptop found with the given id number.')
    laptop = laptops[0]
    laptop.studentid = request.json.get('studentid', laptop.studentid)
    laptop.description = request.json.get('description', laptop.description)
    try:
        laptop.dategiven = datetime.datetime.strptime(request.json.get('dategiven'), '%Y-%m-%d')
    except:
        laptop.dategiven = None
    laptop.comment = request.json.get('comment', laptop.comment)
    db.session.commit()
    return laptop_schema.jsonify(laptop)

@app.route('/laptop', methods=['POST'])
@CheckLogin()
def create_laptop():
    laptop = LaptopModel(
        id = request.json.get('id'),
        studentid = request.json.get('studentid'),
        description = request.json.get('description', ''),
        comment = request.json.get('comment', ''),
    )
    try:
        laptop.dategiven = datetime.datetime.strptime(request.json.get('dategiven'), '%Y-%m-%d')
    except:
        laptop.dategiven = None
    db.session.add(laptop)
    db.session.commit()
    return laptop_schema.jsonify(laptop)

@app.route('/laptop/<number>', methods=['DELETE'])
@CheckLogin()
def delete_laptop(number):
    laptops = LaptopModel.query.filter(LaptopModel.id == number).all()
    if not laptops:
        return Response(status=404, response='No laptop found with the given id number.')
    db.session.delete(laptops[0])
    db.session.commit()
    return laptop_schema.jsonify(laptops[0])

@app.route('/student/<number>/laptops')
@CheckLogin()
def list_laptops_by_student(number):
    laptops = LaptopModel.query.filter(LaptopModel.studentid == number).all()
    return laptops_schema.jsonify(laptops)
