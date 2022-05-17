
import traceback
from json import dumps
from flask import (
    Blueprint, make_response,request
)

from flaskr.db import get_db

bp = Blueprint('client', __name__, url_prefix='/client')


@bp.route('/register', methods=('POST','GET'))
def register():
    if request.method == 'POST':
        db = get_db()
        error = None
        # 获取表单数据
        client_name = request.form['name']
        client_cha = request.form['type']
        discount = request.form['discount']
        contact_man = request.form['contact_man']
        contact_number = request.form['contact_number']
        # 生成客户编号
        num = db.prepare("select count(*) from car_sys.client")
        num = str(num()[0][0])
        num = (4-len(num))*'0'+num
        client_number = 'GS'+num
        try:
            db.execute(
                "INSERT INTO car_sys.client (client_number, client_name, client_cha, discount, contact_man, contact_number) VALUES('{}','{}','{}','{}','{}','{}')".format(
                    client_number, client_name, client_cha, discount, contact_man, contact_number)
            )
        except Exception as e:
            error = traceback.format_exc()
            traceback.print_exc()
            response = make_response(dumps(error), 404)

        else:
            response = make_response(
                dumps('register {} successfully'.format(client_name)), 200)

        return response
    else:
        return 'client/register'


@bp.route('/search', methods=('POST','GET'))
def search():
    if request.method == 'POST':
        db = get_db()
        error = None
        client_number = request.form['number']
        print(client_number)
        if not client_number:
            try:
                rows = db.prepare("select * from car_sys.client ")
            except Exception as e:
                error = traceback.format_exc()
                response = make_response(dumps(error), 404)
            else:
                res = []
                info = rows()
                for row in info:
                    dic = {}
                    dic['client_number'] = row[0]
                    dic['name'] = row[1]
                    dic['type'] = row[2]
                    dic['discount'] = row[3]
                    dic['contact_man'] = row[4]
                    dic['contact_number'] = row[5]
                    res.append(dic)
                
                response = make_response(dumps(res),200)
        else:
            try:
                rows = db.prepare("select * from car_sys.client where client_number='{}'".format(client_number))
            except Exception as e:
                error = traceback.format_exc()
                response = make_response(dumps(error), 404)
            else:
                info = rows()
                # print(info)
                # print(type(info))
                res = []
                dic = {}
                dic['client_number'] = info[0][0]
                dic['name'] = info[0][1]
                dic['type'] = info[0][2]
                dic['discount'] = info[0][3]
                dic['contact_man'] = info[0][4]
                dic['contact_number'] = info[0][5]
                res.append(dic)

                response = make_response(dumps(res),200)
        
        return response
    else:
        return 'client/search'

