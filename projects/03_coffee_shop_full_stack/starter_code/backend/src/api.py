import os
from flask import Flask, request, jsonify, abort
from sqlalchemy import exc
import json
from flask_cors import CORS

from .database.models import db_drop_and_create_all, setup_db, Drink
from .auth.auth import AuthError, requires_auth

app = Flask(__name__)
setup_db(app)
CORS(app)

'''
@TODO uncomment the following line to initialize the datbase
!! NOTE THIS WILL DROP ALL RECORDS AND START YOUR DB FROM SCRATCH
!! NOTE THIS MUST BE UNCOMMENTED ON FIRST RUN
'''
# db_drop_and_create_all()

## ROUTES
'''
@TODO implement endpoint
    GET /drinks
        it should be a public endpoint
        it should contain only the drink.short() data representation
    returns status code 200 and json {"success": True, "drinks": drinks} where drinks is the list of drinks
        or appropriate status code indicating reason for failure
'''
@app.route('/drinks', methods=['GET'])
def get_drinks_short():
    all_drinks = [single_drink.short() for single_drink in Drink.query.all()]
    return jsonify({
        'success': True,
        'drinks': all_drinks
    })

'''
@TODO implement endpoint
    GET /drinks-detail
        it should require the 'get:drinks-detail' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drinks} where drinks is the list of drinks
        or appropriate status code indicating reason for failure
'''
@app.route('/drinks-detail', methods=['GET'])
@requires_auth('get:drinks-detail')
def get_drinks_long():
    try:
        all_drinks = [single_drink.short() for single_drink in Drink.query.all()]
        return jsonify({
            'success': True,
            'drinks': all_drinks
        })
    except:
        abort(500)

'''
@TODO implement endpoint
    POST /drinks
        it should create a new row in the drinks table
        it should require the 'post:drinks' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drink} where drink an array containing only the newly created drink
        or appropriate status code indicating reason for failure
'''
@app.route('/drinks', methods=['POST'])
@requires_auth('post:drinks')
def post_drink():
    try:
        request_body_dict = request.get_json()
        new_drink = Drink(
            title=request_body_dict.get('title'),
            recipe=json.dumps(request_body_dict.get('recipe'))
        )

        new_drink.insert()

        return jsonify(
            {
                'success': True,
                'drinks': [new_drink.long()]
            })
    except Exception as exc:
        abort(400)  # Bad Request


'''
@TODO implement endpoint
    PATCH /drinks/<id>
        where <id> is the existing model id
        it should respond with a 404 error if <id> is not found
        it should update the corresponding row for <id>
        it should require the 'patch:drinks' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drink} where drink an array containing only the updated drink
        or appropriate status code indicating reason for failure
'''
@app.route('/drinks/<int:id>', methods=['PATCH'])
@requires_auth('patch:drinks')
def patch_drink(id):
    try:
        request_body_dict = request.get_json()
        patching_drink = Drink.query.filter(Drink.id == id).one_or_none()

        if not patching_drink:
            abort(404)

        for k, v in request_body_dict.items():
            if k == 'recipe':
                patched_value = json.dumps(v)
            else:
                patched_value = v
            setattr(patching_drink, k, patched_value)

        patching_drink.update()

        return jsonify(
            {
                'success': True,
                'drinks': [patching_drink.long()]
            })
    except Exception as exc:
        abort(400)  # Bad Request


'''
@TODO implement endpoint
    DELETE /drinks/<id>
        where <id> is the existing model id
        it should respond with a 404 error if <id> is not found
        it should delete the corresponding row for <id>
        it should require the 'delete:drinks' permission
    returns status code 200 and json {"success": True, "delete": id} where id is the id of the deleted record
        or appropriate status code indicating reason for failure
'''
@app.route('/drinks/<int:id>', methods=['DELETE'])
@requires_auth('delete:drinks')
def delete_drink(id):
    try:
        deleting_drink = Drink.query.filter(Drink.id == id).one_or_none()

        if not deleting_drink:
            abort(404)

        deleting_drink.delete()

        return jsonify(
            {
                'success': True,
                'drinks': id
            })
    except Exception as exc:
        abort(400)  # Bad Request


## Error Handling
'''
Example error handling for unprocessable entity
'''
@app.errorhandler(422)
def unprocessable(error):
    return jsonify({
                    "success": False, 
                    "error": 422,
                    "message": "unprocessable"
                    }), 422

'''
@TODO implement error handlers using the @app.errorhandler(error) decorator
    each error handler should return (with approprate messages):
             jsonify({
                    "success": False, 
                    "error": 404,
                    "message": "resource not found"
                    }), 404

'''

'''
@TODO implement error handler for 404
    error handler should conform to general task above 
'''
@app.errorhandler(404)
def resource_not_found(error):
    return jsonify({
                    "success": False,
                    "error": 404,
                    "message": "resource not found"
                    }), 404

'''
@TODO implement error handler for AuthError
    error handler should conform to general task above 
'''
@app.errorhandler(401)
def not_authorized(error):
    return jsonify({
                    "success": False,
                    "error": 401,
                    "message": "unauthorized"
                    }), 401

@app.errorhandler(400)
def bad_request(error):
    return jsonify({
        "success": False,
        "error": 400,
        "message": "Bad Request"
    }), 400

@app.errorhandler(500)
def resource_not_found(error):
    return jsonify({
                    "success": False,
                    "error": 500,
                    "message": "internal server error"
                    }), 500

@app.errorhandler(AuthError)
def auth_exception_handler(e: AuthError):
    # Handles all Authorization exceptions
    response = jsonify({
                    "success": False,
                    "error": e.status_code,
                    "message": e.error
                    }), e.status_code
    return response

@app.errorhandler(Exception)
def exception_handler(e: Exception):
    # Handles all exceptions that happen and are not correctly handled
    response = jsonify({
                    "success": False,
                    "error": 500,
                    "message": e.args
                    }), 500
    return response
