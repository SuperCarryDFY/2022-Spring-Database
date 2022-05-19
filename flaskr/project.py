import traceback
from json import dumps
from flask import (
    Blueprint, make_response,request
)

from flaskr.db import get_db

bp = Blueprint('project', __name__, url_prefix='/project')

@bp.route('/search', methods=('POST','GET'))
def search():
    if request.method == 'POST':
        db = get_db()
        error = None
        repair_project_number = request.form['repair_project_number']
        if not repair_project_number:
            try:
                rows = db.prepare("select * from car_sys.repair_project ")
            except Exception as e:
                error = traceback.format_exc()
                response = make_response(dumps(error), 404)
            else:
                res = []
                info = rows()
                for row in info:
                    dic = {}
                    dic['repair_project_number'] = row[0]
                    dic['repair_project'] = row[1]
                    dic['hours'] = row[2]
                    dic['cost'] = row[3]
                    res.append(dic)
                
                response = make_response(dumps(res),200)
        else:
            try:
                rows = db.prepare("select * from car_sys.repair_project where repair_project_number='{}'".format(repair_project_number))
            except Exception as e:
                error = traceback.format_exc()
                response = make_response(dumps(error), 404)
            else:
                info = rows()
                if len(info) == 0:
                    res = "repair_project_number ={} doesn't exist".format(repair_project_number)
                else:
                    res = []
                    dic = {}
                    dic['repair_project_number'] = row[0]
                    dic['repair_project'] = row[1]
                    dic['hours'] = row[2]
                    dic['cost'] = row[3]
                    res.append(dic)

                response = make_response(dumps(res),200)
        
        return response
    else:
        return '/project/search'