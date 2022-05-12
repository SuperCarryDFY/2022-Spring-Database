import sqlite3
import py_opengauss
import click

# g是一个特殊对象，独立于每个请求，把连接储存于其中，可以多次使用
from flask import current_app,g
from flask.cli import with_appcontext

def get_db():
    if 'db' not in g:
        # g.db = sqlite3.connect(
        #     current_app.config['DATABASE'],
        #     detect_types=sqlite3.PARSE_COLNAMES
        # )
        g.db = py_opengauss.open('opengauss://dai:Wsdfy20010@124.223.16.123:5432/car_system')
        g.db.row_factory=sqlite3.Row
    
    return g.db

def close_db(e=None):
    db = g.pop('db',None)

    if db is not None:
        db.close()


def init_db():
    db = get_db()
    # with current_app.open_resource('schema.sql') as f:
    #     db.execute(f.read().decode('utf-8'))

@click.command('init-db')
@with_appcontext
def init_db_commmand():
    "Clear the existing data and create new tables."
    init_db()
    click.echo('Initialized the database.')

def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_commmand)