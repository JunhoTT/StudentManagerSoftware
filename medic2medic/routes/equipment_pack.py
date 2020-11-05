from flask import request, render_template, Response, jsonify, current_app as app
from .. import db
from ..models.student import StudentModel
from ..models.equipment_pack import EquipmentPackModel
from ..models.equipment_pack_content import EquipmentPackContentModel as EPCModel
from ..models.student_pack_content import StudentPackContentsModel as SPCModel
from ..models.student import StudentModel
from google_auth import CheckLogin

from ..schemas.equipment_pack_schema import EquipmentPackSchema

equipment_pack_schema = EquipmentPackSchema()

@app.route('/student/<number>/equipment', methods=['GET'])
@CheckLogin()
def list_student_equipment(number):
    packcontents = SPCModel.query.filter(SPCModel.studentid == number).all()
    return jsonify([pc.packcontents for pc in packcontents])

@app.route('/student/<number>/equipment', methods=['PUT'])
@CheckLogin()
def add_student_equipment(number):
    SPCModel.query.filter(SPCModel.studentid == number).delete()
    for name in request.json:
        contents = SPCModel(studentid=number, packcontents=name)
        db.session.add(contents)
    db.session.commit()
    return jsonify(request.json)

@app.route('/student/<number>/equipmentpack/<name>', methods=['PATCH'])
@CheckLogin()
def update_equipment_pack_name(number, name):
    students = StudentModel.query.filter(StudentModel.id == int(number)).all()
    if not students:
        return Response(status=404, response=f'Student with id "{number}" not found.')
    students[0].equipmentpack = name if name != 'None' else None
    db.session.commit()
    return name

@app.route('/list/equipmentpack')
@CheckLogin()
def list_equipment_packs():
    packs = EquipmentPackModel.query.all()
    contents = EPCModel.query.all()
    return jsonify({
        pack.packname: [content.packcontents for content in contents if content.equipmentpack == pack.packname] for pack in packs
    })

@app.route('/equipmentpack/<name>', methods=['POST'])
@CheckLogin()
def create_equipment_pack(name):
    pack = EquipmentPackModel(packname=name)
    db.session.add(pack)
    db.session.commit()
    return jsonify({'packname': name})

@app.route('/equipmentpack/<name>', methods=['DELETE'])
@CheckLogin()
def delete_equipment_pack(name):
    # Remove equipment pack from students
    students = StudentModel.query.filter(StudentModel.equipmentpack == name).all()
    for student in students:
        student.equipmentpack = None

    studentIds = [ s.id for s in students ]
    
    # Remove student equipment pack contents
    SPCModel.query.filter(SPCModel.studentid in studentIds).delete()
    # Remove equipment pack contents
    EPCModel.query.filter(EPCModel.equipmentpack == name).delete()

    # Commit
    db.session.commit()
    return Response(status=200)

@app.route('/equipmentpack/checkchanges', methods=['POST'])
@CheckLogin()
def check_equipment_pack_contents_changes():
    hasChanges = False
    for pack, contents in request.json.items():
        # Get old contents
        oldContents = [ contents.packcontents for contents in EPCModel.query.filter(EPCModel.equipmentpack == pack).all() ]

        # Check for changes
        hasChanges = hasChanges or not len(oldContents) == len(contents)
        for packcontents in contents:
            hasChanges = hasChanges or packcontents not in oldContents

    # Return number of affected students
    if hasChanges:
        count = 0
        for pack,_ in request.json.items():
            count += StudentModel.query.filter(StudentModel.equipmentpack == pack).count()
        return jsonify({ 'result': count })
    else:
        return jsonify({ 'result': 0 })

@app.route('/equipmentpack/<name>/contents', methods=['PUT'])
@CheckLogin()
def add_equipment_pack_contents(name):
    # Remove references to pack contents that no longer exist
    studentIds = [ s.id for s in StudentModel.query.filter(StudentModel.equipmentpack == name).all() ]
    SPCModel.query.filter(SPCModel.studentid in studentIds and SPCModel.packcontents in request.json).delete()

    # Remove old pack contents
    EPCModel.query.filter(EPCModel.equipmentpack == name).delete()

    # Add new contents
    for packcontents in request.json:
        contents = EPCModel(equipmentpack=name, packcontents=packcontents)
        db.session.add(contents)

    # Commit
    db.session.commit()
    return jsonify(request.json)

@app.route('/equipmentpacks')
@CheckLogin(redirect=True)
def show_equipment_packs():
    return render_template('equipment_packs.html')
