import json

from flask import request

from src.config import app
import src.services as services


@app.route('/cadastrar', methods=['POST'])
def create_route_cadastrar():
    response = json.dumps(request.json)
    res = services.create_data(response)
    return res


@app.route('/modificar-data', methods=['PUT'])
def create_route_modificar():
    response = json.dumps(request.json)
    res = services.update_data(response)
    return res


@app.route('/procurar-fornecedores', methods=['GET'])
def create_route_find():
    res = services.list_all_data()
    return res


@app.route('/deletar-todo-database', methods=['DELETE'])
def create_route_delete_all():
    return services.delete_all_data()


@app.route('/procurar-fornecedores?by=name&by=company', methods=['GET'])
def create_route_find_name_company():
    response = json.dumps(request.json)

    res = services.get_data_name_company(response)
    return res


@app.route('/deletar-fornecedores?by=name&by=company', methods=['DELETE'])
def create_route_delete_name_company():
    response = json.dumps(request.json)
    res = services.delete_data_name_company(response)
    return res


@app.errorhandler(404)
def not_found():
    return services.not_found()


if __name__ == "__main__":
    app.run(port=8080, debug=True)
