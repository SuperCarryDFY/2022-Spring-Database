import traceback
from json import dumps
from flask import (
    Blueprint, make_response, request
)

from flaskr.db import get_db

bp = Blueprint('order', __name__, url_prefix='/order')


def get_repair_number():
    db = get_db()
    rows = db.prepare("select * from car_sys.repair_order;")
    info = rows()
    if len(info) == 0:
        return 1
    else:
        repair_number_list = []
        for record in info:
            repair_number_list.append(record[-1])
        return max(repair_number_list)+1



@bp.route('/register', methods=('POST', 'GET'))
def register():

    if request.method == 'POST':
        db = get_db()
        error = None
        # 获取表单数据
        repair_cha = request.form['repair_type']
        job_classify = request.form['job_type']
        pay_method = request.form['pay_method']
        car_arch = request.form['VLN']
        mileage = request.form['mileage']
        oil_mass = request.form['oil_mass']
        begin_time = request.form['begin_time']
        salesman_number = request.form['salesman_number']
        end_time = request.form['end_time']
        breakdown_des = request.form['breakdown_des']
        status = request.form['status']
        repair_number = get_repair_number()
        if not salesman_number:
            error = 'salesman_number is required.'
        if not car_arch:
            error = 'VLN is required.'
        if error:
            return make_response(dumps(error), 404)

        try:
            # 这里写sql插入语句
            db.execute(
                "INSERT INTO car_sys.repair_order (repair_cha, job_classify, pay_method, car_arch, mileage,oil_mass,begin_time,salesman_number, end_time, breakdown_des, repair_number,status) VALUES('{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}')".format(
                    repair_cha, job_classify, pay_method, car_arch, mileage, oil_mass, begin_time, salesman_number, end_time, breakdown_des, repair_number, status)
            )

        except Exception as e:
            error = traceback.format_exc()
            traceback.print_exc()
            response = make_response(dumps(error), 404)
        else:
            repair_dic={'repair_number':repair_number}
            response = make_response(
                dumps(repair_dic), 200)

        return response
    else:
        return '/order/register'


@bp.route('/search', methods=('POST', 'GET'))
def search():
    if request.method == 'POST':
        db = get_db()
        error = None
        car_arch = request.form['VLN']
        begin_time = request.form['begin_time']
        if not car_arch:
            try:
                rows = db.prepare("select * from car_sys.repair_order join car_sys.car_info on repair_order.car_arch=car_info.car_arch")
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
                response = make_response(dumps(res), 200)
        else:
            try:
                rows = db.prepare(
                    "select * from car_sys.repair_order join car_sys.car_info on repair_order.car_arch=car_info.car_arch where repair_order.car_arch='{}' and repair_order.begin_time='{}'".format(car_arch,begin_time))
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
                # print("res\n")
                # print(res)
                # print('\n')
                response = make_response(dumps(res), 200)
        return response
    else:
        return '/order/search'


@bp.route('/change', methods=('POST', 'GET'))
def change():
    if request.method == 'POST':
        db = get_db()
        error = None

        repair_cha = request.form['repair_type']
        job_classify = request.form['job_type']
        pay_method = request.form['pay_method']
        mileage = request.form['mileage']
        oil_mass = request.form['oil_mass']
        begin_time = request.form['begin_time']
        end_time = request.form['end_time']
        breakdown_des = request.form['breakdown_des']
        repair_number = request.form['repair_number']
        cost = request.form['cost']
        status = request.form['status']
        if not repair_number:
            error = 'repair_number is required.'
        try:
            db.execute("UPDATE car_sys.repair_order set repair_cha={}, job_classify={}, pay_method='{}', mileage={}, oil_mass={}, begin_time='{}', end_time='{}', breakdown_des='{}',cost={},status='{}' where repair_number='{}'".format(
                repair_cha, job_classify, pay_method, mileage, oil_mass, begin_time, end_time, breakdown_des, cost, status, repair_number))
        except Exception as e:
            error = traceback.format_exc()
            response = make_response(dumps(error), 404)
        else:
            response = make_response(dumps("update order successfully"), 200)
        return response

    else:
        return '/order/change'
