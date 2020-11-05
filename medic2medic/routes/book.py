from flask import request, render_template, make_response, jsonify, Response
from datetime import datetime as dt
from flask import current_app as app
#from .student import db, User
from ..schemas.book_schema import BookSchema
from ..models.book import BookModel
from .. import db
import datetime
from google_auth import CheckLogin

book_schema = BookSchema()
books_schema = BookSchema(many=True)

@app.route('/book/')
@CheckLogin()
def book_list():
    all_books = BookModel.query.all()
    return jsonify(books_schema.dump(all_books))

@app.route('/book/<number>')
@CheckLogin()
def book_by_number(number):
    books = BookModel.query.filter(BookModel.id == number).all()
    return jsonify(book_schema.dump(books[0]))



@app.route('/book/', methods=['POST'])
@CheckLogin()
def create_book():
    book = BookModel(
        title=request.json.get('title'),
        author=request.json.get('author'),
    )
    db.session.add(book)
    db.session.commit()
    return book_schema.jsonify(book)

@app.route('/book/<number>', methods=['PATCH'])
@CheckLogin()
def update_book(number):
    books = BookModel.query.filter(BookModel.id == number).all()
    if not books:
        return Response(status=404, response='No laptop found with the given id number.')
    book = books[0]
    book.studentid = request.json.get('studentid', book.studentid)
    book.title = request.json.get('title', book.title)
    book.author = request.json.get('author', book.author)
    try:
        book.dategiven = datetime.datetime.strptime(request.json.get('dategiven'), '%Y-%m-%d')
    except:
        book.dategiven = None


    db.session.commit()
    return book_schema.jsonify(book)

@app.route('/book/<id>', methods=['DELETE'])
def delete_book(id):
    BookModel.query.filter_by(id=id).delete()
    db.session.commit()
    all_books = BookModel.query.all()
    return jsonify(books_schema.dump(all_books))

@app.route('/list/books')
@CheckLogin(redirect=True)
def list_books():
    return render_template('books.html')

@app.route('/edit/book/<number>')
@CheckLogin(redirect=True)
def edit_book(number):
    books = BookModel.query.filter(BookModel.id == number).all()
    if not books:
        return render_template('not_found.html')
    return render_template('book.html', id=number)
