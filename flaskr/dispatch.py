import traceback
from json import dumps
from flask import (
    Blueprint, make_response, request
)

from flaskr.db import get_db

bp = Blueprint('dispatch', __name__, url_prefix='/dispatch')


@bp.route('/register', methods=('POST', 'GET'))
def register():
    if request.method == 'POST':
        db = get_db()
        error = None
        # 获取表单数据
        repair_number = request.form['repair_number']
        repair_man_number = request.form['repair_man_number']
        repair_project_number = request.form['repair_project_number']

        try:
            db.execute(
                "INSERT INTO car_sys.repair_dispatch (repair_number, repair_man_number, repair_project_number) VALUES('{}','{}','{}')".format(
                    repair_number, repair_man_number,repair_project_number)
            )
        except Exception as e:
            error = traceback.format_exc()
            traceback.print_exc()
            response = make_response(dumps(error), 404)
        else:
            response = make_response(
                dumps('create dispatch successfully'), 200)
        return response

    else:
        return '/dispatch/register'


@bp.route('/search', methods=('POST','GET'))
def search():
    if request.method == 'POST':
        db = get_db()
        error = None
        repair_number = request.form['repair_number']
        repair_man_number = request.form['repair_man_number']
        try:
            if not repair_number and not repair_man_number:
                rows = db.prepare("select A.repair_number, A.repair_project_number, C.repair_project, C.hours, B.id, B.repair_man_classify, C.cost  from car_sys.repair_dispatch as A, car_sys.repairman as B, car_sys.repair_project as C  where B.id=A.repair_man_number and C.repair_project_number=A.repair_project_number")
            elif not repair_number:
                rows = db.prepare("select A.repair_number, A.repair_project_number, C.repair_project, C.hours, B.id, B.repair_man_classify, C.cost  from car_sys.repair_dispatch as A, car_sys.repairman as B, car_sys.repair_project as C  where B.id=A.repair_man_number and C.repair_project_number=A.repair_project_number and  A.repair_man_number={}".format(repair_man_number))
            elif not repair_man_number:
                rows = db.prepare("select A.repair_number, A.repair_project_number, C.repair_project, C.hours, B.id, B.repair_man_classify, C.cost  from car_sys.repair_dispatch as A, car_sys.repairman as B, car_sys.repair_project as C  where B.id=A.repair_man_number and C.repair_project_number=A.repair_project_number and  A.repair_number={}".format(repair_number))
            else:
                rows = db.prepare("select A.repair_number, A.repair_project_number, C.repair_project, C.hours, B.id, B.repair_man_classify, C.cost  from car_sys.repair_dispatch as A, car_sys.repairman as B, car_sys.repair_project as C  where B.id=A.repair_man_number and C.repair_project_number=A.repair_project_number and  A.repair_man_number={} and  A.repair_number={}".format(repair_man_number,repair_number))
        except Exception as e:
            error = traceback.format_exc()
            response = make_response(dumps(error), 404) 
        else:
            res = []
            info = rows()
            column_names = rows.column_names
            for row in info:
                dic = {}
                for i in range(len(column_names)):
                    dic[column_names[i]] = row[i]
                res.append(dic)
            response = make_response(dumps(res),200)
        return response
    else:
        return 'dispatch/search'



@bp.route('/delete', methods=('DELETE','GET'))
def delete():
    if request.method == 'DELETE':
        db = get_db()
        error = None
        repair_number = request.form['repair_number']
        try:
            db.execute("DELETE from car_sys.repair_dispatch where repair_number={}".format(repair_number))
            
        except Exception as e:
            error = traceback.format_exc()
            response = make_response(dumps(error), 404)
        else:
            response = make_response(dumps('delete repair_number={} successfully!'.format(repair_number)))
        return response


    else:
        return '/dispatch/delete'