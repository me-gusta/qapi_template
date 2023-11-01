from hashlib import sha256

from bson import ObjectId
from flask import request, render_template
from flask_cors import cross_origin
from flask_login import login_required, login_user

from server import app, csrf
from website.admin_settings import admin_views
from website.authentication import user, is_authenticated
from website.qapi.component import Component
from website.qapi.database import db
from website.qapi.queries import my_query_to_mongodb, clear_cache


def make_hash(s: str) -> str:
    return sha256(s.encode('utf-8')).hexdigest()


@app.route("/qapi/admin", methods=['GET', 'POST'])
def admin_page():
    context = {
        'url': 'http://91.142.74.196/'
    }

    if app.debug:
        context['url'] = 'http://127.0.0.1:5000/'
        login_user(user)

    if is_authenticated():
        return render_template('pages/admin.html', **context)

    password_hash = '2d98b5080f2580c256e8a0042f570c149dd8942ec89230374383a5cec0c50371'

    if request.method == 'POST':
        data = dict(request.form)
        if data['username'] == 'admin' and make_hash(data['password']) == password_hash:
            login_user(user)
            return render_template('pages/admin.html', **context)

    return render_template('pages/admin_login.html')


@app.route('/qapi/getAdminInfo', methods=['POST'])
@cross_origin()
@csrf.exempt
@login_required
def get_admin_info():
    return {'ok': True, 'views': admin_views}


@app.route('/qapi/queryPull', methods=['POST'])
@cross_origin()
@csrf.exempt
@login_required
def query_pull_route():
    def debsonify(x):
        x['_id'] = str(x['_id'])
        return x

    data = request.get_json()
    query = data['query']
    tb_query = my_query_to_mongodb(query)
    projection = {x['name']: True for x in query}

    cursor = db.find(tb_query, projection)
    if data.get('sort'):
        cursor.sort(data.get('sort'))

    fields = [debsonify(x) for x in cursor]

    return {'ok': True, 'fields': fields}


@app.route('/qapi/queryPush', methods=['POST'])
@cross_origin()
@csrf.exempt
@login_required
def query_push_route():
    def debsonify(x):
        out = {'_id': ObjectId(x['_id'])}
        del x['_id']
        return out

    tb_query = request.get_json()
    print(tb_query)
    all_components = Component.all
    for ent in tb_query:
        for component_name, value in ent.copy().items():
            t = all_components.get(component_name)
            if t is None:
                continue
            if t == int:
                ent[component_name] = int(ent[component_name])

    for q in tb_query:
        db.update_one(debsonify(q), {'$set': q})
    # projection = {x['name']: True for x in data}
    # projection['_id'] = False
    # fields = list(db.find(tb_query, projection))
    clear_cache()

    return {'ok': True, 'fields': 'fields'}


@app.route('/qapi/querySet', methods=['POST'])
@cross_origin()
@csrf.exempt
@login_required
def query_set_route():
    data = request.get_json()
    query = my_query_to_mongodb(data['query'])
    set_cmd = data['set']
    db.update_many(query, {'$set': set_cmd})
    clear_cache()

    return {'ok': True}


@app.route('/qapi/querySetSelected', methods=['POST'])
@cross_origin()
@csrf.exempt
@login_required
def query_set_selected_route():
    data = request.get_json()
    ids = data['ids']
    set_cmd = data['command']

    for bson_id in ids:
        db.update_one({'_id': ObjectId(bson_id)}, {'$set': set_cmd})

    clear_cache()

    return {'ok': True}
