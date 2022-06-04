import traceback
from json import dumps
from flask import (
    Blueprint, make_response, request
)

from flaskr.db import get_db

bp = Blueprint('repair_material', __name__, url_prefix='/repair_material')

@bp.route('/add',methods=('POST','GET'))
def add():
    if request.method == 'POST':
        db = get_db()
        error = None
        repair_number = request.form['repair_number']
        material_name = request.form['material_name']
        if not repair_number or not material_name:
            error = "material_name and repair_name is required."
            return make_response(dumps(error),404)
        try:
            db.execute(
                "INSERT INTO car_sys.repair_material(repair_number,material_name) VALUES({},'{}')".format(repair_number,material_name)
            )
        except Exception as e:
            error = traceback.format_exc()
            traceback.print_exc()
            response = make_response(dumps(error), 404)
        else:
            response=make_response(dumps('add repair_number:{} and material_name:{} successfully.'.format(repair_number,material_name)),200)

        return response
    else:
        return 'repair_material/add'


@bp.route('/search', methods=('POST','GET'))
def search():
    if request.method == 'POST':
        db = get_db()
        error = None
        repair_number = request.form['repair_number']
        if not repair_number:
            rows = db.prepare("SELECT * from car_sys.repair_material")
        else:
            rows = db.prepare("SELECT * from car_sys.repair_material where repair_number={}".format(repair_number))
        column_names = rows.column_names
        res = []
        for row in rows():
            dic = {}
            for i in range(len(column_names)):
                dic[column_names[i]] = row[i]
            res.append(dic)
        response = make_response(dumps(res),200)
        return response
    else:
        return 'repair_material/search'
