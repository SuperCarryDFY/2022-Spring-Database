from genericpath import exists
import traceback
from json import dumps
from flask import (
    Blueprint, make_response,request
)

from flaskr.db import get_db

bp = Blueprint('staff', __name__, url_prefix='/staff')

@bp.route('/repairman/search', methods=('POST','GET'))
def repairman_search():
    if request.method == 'POST':
        db = get_db()
        error = None
        id = request.form['id']
        if not id:
            try:
                rows = db.prepare("select * from car_sys.repairman ")
            except Exception as e:
                error = traceback.format_exc()
                response = make_response(dumps(error), 404)
            else:
                res = []
                info = rows()
                for row in info:
                    dic = {}
                    dic['id'] = row[0]
                    dic['type'] = row[1]
                    dic['name'] = row[2]
                    dic['telephone'] = row[3]
                    res.append(dic)
                
                response = make_response(dumps(res),200)
        else:
            try:
                rows = db.prepare("select * from car_sys.repairman where id='{}'".format(id))
            except Exception as e:
                error = traceback.format_exc()
                response = make_response(dumps(error), 404)
            else:
                info = rows()
                if len(info) == 0:
                    res = "id={} doesn't exist".format(id)
                else:
                    res = []
                    dic = {}
                    dic['id'] = info[0][0]
                    dic['type'] = info[0][1]
                    dic['name'] = info[0][2]
                    dic['telephone'] = info[0][3]
                    res.append(dic)

                response = make_response(dumps(res),200)
        
        return response
    else:
        return 'staff/repairman/search'


@bp.route('/salesman/search', methods=('POST','GET'))
def salesman_search():
    if request.method == 'POST':
        db = get_db()
        error = None
        id = request.form['id']
        if not id:
            try:
                rows = db.prepare("select * from car_sys.salesman ")
            except Exception as e:
                error = traceback.format_exc()
                response = make_response(dumps(error), 404)
            else:
                res = []
                info = rows()
                for row in info:
                    dic = {}
                    dic['id'] = row[0]
                    dic['name'] = row[1]
                    dic['telephone'] = row[2]
                    res.append(dic)
                
                response = make_response(dumps(res),200)
        else:
            try:
                rows = db.prepare("select * from car_sys.salesman where id='{}'".format(id))
            except Exception as e:
                error = traceback.format_exc()
                response = make_response(dumps(error), 404)
            else:
                info = rows()
                if len(info) == 0:
                    res = "id = {} doesn't exist".format(id)
                else:
                    res = []
                    dic = {}
                    dic['id'] = info[0][0]
                    dic['name'] = info[0][1]
                    dic['telephone'] = info[0][2]
                    res.append(dic)

                response = make_response(dumps(res),200)
        
        return response
    else:
        return 'staff/salesman/search'
