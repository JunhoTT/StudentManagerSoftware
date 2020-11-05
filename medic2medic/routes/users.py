from flask import request, render_template
from flask import current_app as app
from ..schemas.user_schema import UserSchema
from ..models.user import UserModel, setup_admin
from .. import db
from google_auth import CheckLogin

users_schema = UserSchema(many=True)

@app.route('/list/user')
@CheckLogin(requiredPermissions=['read', 'admin'])
def list_users():
    users = UserModel.query.all()
    return users_schema.jsonify(users)

@app.route('/users', methods=['PUT'])
@CheckLogin(requiredPermissions=['write', 'admin'])
def update_users():
    UserModel.query.delete()
    for user_json in request.json:
        user = UserModel(
            email = user_json.get('email'),
            permissions = str(user_json.get('permissions'))
        )
        db.session.add(user)
    db.session.commit()
    setup_admin()
    return users_schema.jsonify(request.json)

@app.route('/users', methods=['GET'])
@CheckLogin(requiredPermissions=['read', 'write', 'admin'], redirect=True)
def users():
    return render_template('users.html')
