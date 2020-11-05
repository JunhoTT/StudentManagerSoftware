from flask import request, render_template, make_response, jsonify
from datetime import datetime as dt
from flask import current_app as app
#from .student import db, User
from ..schemas.uni_schema import UniSchema
from ..models.university import UniModel
from .. import db
from google_auth import CheckLogin

uni_schema = UniSchema()
unis_schema = UniSchema(many=True)
@app.route('/university/')
@CheckLogin()
def uni_list():
    all_unis = UniModel.query.all()
    return jsonify(unis_schema.dump(all_unis))

@app.route('/university/<number>')
@CheckLogin()
def uni_by_number(number):
    unis = UniModel.query.filter(UniModel.id == number).all()
    return jsonify(uni_schema.dump(unis[0]))


@app.route('/university/', methods=['POST'])
@CheckLogin()
def create_uni():
    uni_name = request.json.get('uni_name', '')
    country = request.json.get('country', '')

    uni = UniModel(
        uni_name=uni_name,
        country=country,
    )
    db.session.add(uni)
    db.session.commit()
    return uni_schema.jsonify(uni)

@app.route('/university/', methods=['PATCH'])
@CheckLogin()
def update_uni():
    uni_name = request.json.get('uni_name', '')
    country = request.json.get('country', '')
    id = request.json.get('id', '')

    unis = UniModel.query.filter(UniModel.id == id).all()

    uni = unis[0]
    uni.uni_name = uni_name
    uni.country = country
    db.session.commit()
    return uni_schema.jsonify(uni)

@app.route('/university/<id>', methods=['DELETE'])
def delete_uni(id):
    UniModel.query.filter_by(id=id).delete()
    db.session.commit()
    all_unis = UniModel.query.all()
    return jsonify(unis_schema.dump(all_unis))

@app.route('/list/universities')
@CheckLogin(redirect=True)
def list_unis():
    return render_template('universities.html')

@app.route('/edit/university/<number>')
@CheckLogin(redirect=True)
def edit_uni(number):
    unis = UniModel.query.filter(UniModel.id == number).all()
    if not unis:
        return render_template('not_found.html')
    return render_template('university.html', id=number)
