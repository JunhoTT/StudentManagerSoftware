from flask import request, jsonify, current_app as app
from .. import db
from ..models.quotes import QuoteModel
from google_auth import CheckLogin

@app.route('/student/<number>/quotes', methods=['GET'])
@CheckLogin()
def get_quotes(number):
    quotes = QuoteModel.query.filter(QuoteModel.studentid == number).all()
    return jsonify([quote.text for quote in quotes])

@app.route('/student/<number>/quotes', methods=['PUT'])
@CheckLogin()
def delete_quote(number):
    QuoteModel.query.filter(QuoteModel.studentid == number).delete()
    for quote in request.json:
        db.session.add(QuoteModel(studentid=number, text=quote))
    db.session.commit()
    return jsonify(request.json)