import traceback
from json import dumps
from flask import (
    Blueprint, make_response,request
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
        return rows()[-1][-1]+1

@bp.route('/register', methods=('POST','GET'))
def register():

    if request.method == 'POST':
        db = get_db()
        error = None
        # 获取表单数据
        client_number = request.form['Gnumber']
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
        repair_number = get_repair_number()
        if not client_number:
            error = 'Gnumber is required.'
        if not car_arch:
            error = 'VLN is required.'
        if error :
            return make_response(dumps(error), 404)


        try :
            # 这里写sql插入语句
            db.execute(
                "INSERT INTO car_sys.repair_order (client_number, repair_cha, job_classify, pay_method, car_arch, mileage,oil_mass,begin_time,salesman_number, end_time, breakdown_des, repair_number) VALUES('{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}')".format(
                    client_number, repair_cha, job_classify, pay_method, car_arch, mileage, oil_mass, begin_time, salesman_number, end_time, breakdown_des,repair_number)
            )
            
        except Exception as e:
            error = traceback.format_exc()
            traceback.print_exc()
            response = make_response(dumps(error), 404)
        else:  
            response = make_response(
                dumps('repair_number:{} insert successfully'.format(repair_number)), 200)
        
        return response
    else:
        return '/order/register'


@bp.route('/search', methods=('POST','GET'))
def search():
    if request.method == 'POST':
        db = get_db()
        error = None
        client_number = request.form['Gnumber']
        if not client_number:
            try:
                rows = db.prepare("select * from car_sys.repair_order")
            except Exception as e:
                error = traceback.format_exc()
                response = make_response(dumps(error), 404)  
            else:
                res = []
                info = rows()
                for row in info:
                    dic = {}
                    dic['Gnumber'] = row[0]
                    dic['repair_type'] = row[1]
                    dic['job_type'] = row[2]
                    dic['pay_method'] = row[3]
                    dic['VLN'] = row[4]
                    dic['mileage'] = row[5]
                    dic['oil_mass'] = row[6]
                    dic['begin_time'] = row[7]
                    dic['salesman_number'] = row[8]
                    dic['end_time'] = row[9]
                    dic['breakdown_des'] = row[10]
                    res.append(dic)
                
                response = make_response(dumps(res),200)
        else:
            try:
                rows = db.prepare("select * from car_sys.repair_order where client_number='{}'".format(client_number))
            except Exception as e:
                error = traceback.format_exc()
                response = make_response(dumps(error), 404)
            else:
                res = []
                info = rows()
                for row in info:
                    dic = {}
                    dic['Gnumber'] = row[0]
                    dic['repair_type'] = row[1]
                    dic['job_type'] = row[2]
                    dic['pay_method'] = row[3]
                    dic['VLN'] = row[4]
                    dic['mileage'] = row[5]
                    dic['oil_mass'] = row[6]
                    dic['begin_time'] = row[7]
                    dic['salesman_number'] = row[8]
                    dic['end_time'] = row[9]
                    dic['breakdown_des'] = row[10]
                    dic['repair_number'] = row[11]
                    res.append(dic)
                response = make_response(dumps(res),200)
        return response
    else:
        return '/order/search'