import traceback
from json import dumps
from flask import (
    Blueprint, make_response, request
)

from flaskr.db import get_db

bp = Blueprint('car', __name__, url_prefix='/car')


@bp.route('/register', methods=('POST', 'GET'))
def register():
    if request.method == 'POST':
        # 获取表单

        car_arch = request.form['VLN']
        car_number = request.form['carNo']
        car_color = request.form['color']
        car_type = request.form['carType']
        car_class = request.form['carClass']
        client_number = request.form['Gnumber']
        status = request.form['status']

        db = get_db()
        error = None

        # VLN和carNo是要求的，其他没填的设置为默认值
        if not car_arch:
            error = 'VLN is required.'
        if not client_number:
            error = 'Gnumber is required.'

        if error is None:
            try:
                db.execute(
                    "INSERT INTO car_sys.car_info (car_number,car_arch,car_color,car_type,car_class,client_number,status) VALUES('{}','{}','{}','{}','{}','{}','{}')".format(
                        car_number, car_arch, car_color, car_type, car_class, client_number, status)
                )

            except Exception as e:
                traceback.print_exc()
                error = f"Car {car_arch} is already registered or the User{client_number} doesn't exits"
                response = make_response(dumps(error), 400)
            else:
                response = make_response(
                    dumps('register {} successfully'.format(car_arch)), 200)
        else:
            response = make_response(dumps(error), 400)
        return response
    else:
        return 'car/register'


@bp.route('/search', methods=('POST', 'GET'))
def search():
    if request.method == 'POST':
        db = get_db()
        error = None
        car_arch = request.form['VLN']
        if not car_arch:
            try:
                rows = db.prepare("select * from car_sys.car_info")
            except Exception as e:
                error = traceback.format_exc()
                response = make_response(dumps(error), 404)
            else:
                res = []
                info = rows()
                for row in info:
                    dic = {}
                    dic['carNo'] = row[0]
                    dic['VLN'] = row[1]
                    dic['color'] = row[2]
                    dic['carType'] = row[3]
                    dic['carClass'] = row[4]
                    dic['Gnumber'] = row[5]
                    dic['status'] = row[6]
                    res.append(dic)

                response = make_response(dumps(res), 200)
        else:
            try:
                rows = db.prepare(
                    "select * from car_sys.car_info where car_arch='{}'".format(car_arch))
            except Exception as e:
                error = traceback.format_exc()
                response = make_response(dumps(error), 404)
            else:
                res = []
                info = rows()
                for row in info:
                    dic = {}
                    dic['carNo'] = row[0]
                    dic['VLN'] = row[1]
                    dic['color'] = row[2]
                    dic['carType'] = row[3]
                    dic['carClass'] = row[4]
                    dic['Gnumber'] = row[5]
                    dic['status'] = row[6]
                    res.append(dic)
                response = make_response(dumps(res), 200)
        return response
    else:
        return 'car/search'


@bp.route('/search_Gnumber', methods=('POST', 'GET'))
def search_Gnumber():
    if request.method == 'POST':
        db = get_db()
        error = None
        client_number = request.form['Gnumber']
        if not client_number:
            try:
                rows = db.prepare("select * from car_sys.car_info")
            except Exception as e:
                error = traceback.format_exc()
                response = make_response(dumps(error), 404)
            else:
                res = []
                info = rows()
                for row in info:
                    dic = {}
                    dic['carNo'] = row[0]
                    dic['VLN'] = row[1]
                    dic['color'] = row[2]
                    dic['carType'] = row[3]
                    dic['carClass'] = row[4]
                    dic['Gnumber'] = row[5]
                    dic['status'] = row[6]
                    res.append(dic)

            response = make_response(dumps(res), 200)
        else:
            try:
                rows = db.prepare(
                    "select * from car_sys.car_info where client_number='{}'".format(client_number))
            except Exception as e:
                error = traceback.format_exc()
                response = make_response(dumps(error), 404)
            else:
                res = []
                info = rows()
                for row in info:
                    dic = {}
                    dic['carNo'] = row[0]
                    dic['VLN'] = row[1]
                    dic['color'] = row[2]
                    dic['carType'] = row[3]
                    dic['carClass'] = row[4]
                    dic['Gnumber'] = row[5]
                    dic['status'] = row[6]
                    res.append(dic)
                response = make_response(dumps(res), 200)

        return response
    else:
        return 'car/search_Gnumber'


@bp.route('/ChangeStatus', methods=('POST', 'GET'))
def ChangeStatus():
    if request.method == 'POST':
        db = get_db()
        error = None
        car_arch = request.form['VLN']
        status = request.form['status']
        try:
            db.execute("UPDATE car_sys.car_info set status={} where car_arch='{}'".format(
                status, car_arch))

        except Exception as e:
            error = traceback.format_exc()
            traceback.print_exc()
            response = make_response(dumps(error), 404)

        else:
            response = make_response(
                dumps('change successfully'), 200)
        return response

    else:
        return '/car/change_status'


@bp.route('/update', methods=("POST", "GET"))
def delete():
    if request.method == "POST":
        error = None
        db = get_db()
        car_arch = request.form['VLN']
        car_number = request.form['carNo']
        car_color = request.form['color']
        car_type = request.form['carType']
        car_class = request.form['carClass']
        client_number = request.form['Gnumber']
        try:
            db.execute("UPDATE car_sys.car_info set car_number='{}', car_color='{}', car_type='{}', car_class='{}', client_number='{}' where car_arch='{}'".format(
                car_number, car_color, car_type, car_class, client_number,car_arch))
        except Exception as e:
            error = traceback.format_exc()
            response = make_response(dumps(error), 404)
        else:
            response = make_response(
                dumps("update VLN={} successfully".format(car_arch)), 200)
        return response

    else:
        return '/car/update'
