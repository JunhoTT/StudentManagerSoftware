from flask import request, Response, current_app as app
from .. import db
from ..models.tuition import TuitionModel
from ..schemas.tuition_schema import TuitionSchema
from google_auth import CheckLogin

tuition_schema = TuitionSchema()
tuitions_schema = TuitionSchema(many=True)

@app.route('/tuition/<number>', methods=['GET'])
@CheckLogin()
def get_tuition(number):
    tuitions = TuitionModel.query.filter(TuitionModel.id == number).all()
    if not tuitions:
        return Response(status=404, response='No tuition fees found with the given id number.')
    return tuition_schema.jsonify(tuitions[0])

@app.route('/tuition/<number>', methods=['PATCH'])
@CheckLogin()
def update_tuition(number):
    tuitions = TuitionModel.query.filter(TuitionModel.id == number).all()
    if not tuitions:
        return Response(status=404, response='No tuition fees found with the given id number.')
    tuition = tuitions[0]
    tuition.studentid = request.json.get('studentid', tuition.studentid)
    tuition.year = request.json.get('year', tuition.year)
    tuition.feestructure = request.json.get('feestructure', tuition.feestructure)
    tuition.partialscholarship = request.json.get('partialscholarship', tuition.partialscholarship)
    tuition.feebalance = request.json.get('feebalance', tuition.feebalance)
    tuition.feepaid = request.json.get('feepaid', tuition.feepaid)
    db.session.commit()
    return tuition_schema.jsonify(tuition)

@app.route('/tuition', methods=['POST'])
@CheckLogin()
def create_tuition():
    tuition = TuitionModel(
        id = request.json.get('id'),
        studentid = request.json.get('studentid'),
        year = request.json.get('year', ''),
        feestructure = request.json.get('feestructure', ''),
        partialscholarship = request.json.get('partialscholarship', ''),
        feebalance = request.json.get('feebalance', ''),
        feepaid = request.json.get('feepaid', ''),
    )
    db.session.add(tuition)
    db.session.commit()
    return tuition_schema.jsonify(tuition)

@app.route('/tuition/<number>', methods=['DELETE'])
@CheckLogin()
def delete_tuition(number):
    tuitions = TuitionModel.query.filter(TuitionModel.id == number).all()
    if not tuitions:
        return Response(status=404, response='No tuition fees found with the given id number.')
    db.session.delete(tuitions[0])
    db.session.commit()
    return tuition_schema.jsonify(tuitions[0])

@app.route('/student/<number>/tuitions')
@CheckLogin()
def list_tuitions_by_student(number):
    tuitions = TuitionModel.query.filter(TuitionModel.studentid == number).all()
    return tuitions_schema.jsonify(tuitions)
