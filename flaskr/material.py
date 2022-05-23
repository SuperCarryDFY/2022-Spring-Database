from json import dumps
from flask import (
    Blueprint, make_response,request
)

from flaskr.db import get_db

bp = Blueprint('material',__name__,url_prefix='/material')

@bp.route('/search',methods=('POST','GET'))
def search():
    if request.method == 'POST':
        db = get_db()
        error = None
        material_name = request.form['material_name']
        if not material_name:
            rows = db.prepare('select * from car_sys.material')
        else:
            rows = db.prepare("select * from car_sys.material where material_name='{}'".format(material_name))
        
        res = []
        info = rows()
        for row in info:
            dic = {}
            dic['material_name'] = row[0]
            dic['material_cost'] = row[1]
            res.append(dic)
        
        response = make_response(dumps(res),200)
        return response
    else:
        return '/material/search'
