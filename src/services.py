import json
import string
import random
from datetime import datetime
from bson import json_util
from flask import Response, request, jsonify
from src.config import mongo


def random_generator(size=16, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


def exists_data(self):
    r = json.loads(self)
    name = r['name']
    company = r['company']
    product = r['product']
    return mongo.db.user.find_one({'name': name, 'company': company, 'product': product})

def create_data(self):
    r = json.loads(self)
    name = r['name']
    company = r['company']
    amount_products = r['amount_products']
    product = r['product']

    exists = exists_data(self)

    if exists:
        response = json_util.dumps({'message': 'Já existe um fornecedor cadastrado com este nome, companhia e produto.'})
        return Response(response, mimetype='application/json', status=400)

    data_now = datetime.now().isoformat()
    created_at = datetime.fromisoformat(data_now).strptime()

    id = random_generator()

    mongo.db.user.insert_one(
        {'_id': id, 'name': name, 'company': company, 'created_at': (created_at),
         'amount_products': int(amount_products), 'product': product}
    )
    jsonData = {
        '_id': id,
        'name': name,
        'company': company,
        'created_at': created_at,
        'amount_products': int(amount_products),
        'product': product
    }
    response = json_util.dumps(jsonData)
    return Response(response, mimetype='application/json', status=201)


def update_data(self):
    r = json.loads(self)
    name = r['name']
    company = r['company']
    amount_products = r['amount_products']
    product = r['product']

    exists = exists_data(self)

    if not exists:
        return not_found()

    mongo.db.user.update_one(
        {'name': name, 'company': company, 'amount_products': int(amount_products), 'product': product}
    )
    jsonData = {
        '_id': exists['_id'],
        'name': name,
        'company': company,
        'created_at': exists['created_at'],
        'amount_products': int(amount_products),
        'product': product
    }
    response = json_util.dumps(jsonData)
    return Response(response, mimetype='application/json', status=201)


def list_all_data():
    data = mongo.db.user.find()
    if data:
        response = json_util.dumps(data)
        return Response(response, mimetype='application/json', status=302)
    else:
        return not_found()


def get_data_name_company(self):
    r = json.loads(self)
    name = r['name']
    company = r['company']
    data = mongo.db.user.find_one({'name': name, 'company': company})

    if data:
        resp = json_util.dumps(data)
        return Response(resp, mimetype="application/json", status=302)
    else:
        return not_found()


def delete_data_name_company(self):
    r = json.loads(self)
    name = r['name']
    company = r['company']

    exists = exists_data(self)

    if not exists:
        return not_found()

    mongo.db.user.delete_one({'_id':exists['_id'], 'name': name, 'company': company})
    response = jsonify({'message': 'Fornecedores -- name= ' + name + ' && company= ' + company + ' Deleted Successfully'})
    response.status_code = 200
    return response


def delete_all_data():
    mongo.db.user.delete_many({})
    response = jsonify({'message': 'All data Deleted Successfully'})
    response.status_code = 200
    return response


def not_found(error=None):
    message = {
        'message': 'Data Not Found ',
        'status': 404
    }
    response = jsonify(message)
    response.status_code = 404
    return response
