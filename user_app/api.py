import flask, flask_cors, json, os, sys, time
from flask import request, jsonify
from flask_cors import CORS, cross_origin, CORS
from models import *
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt
import logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s')
logger=logging.getLogger(__name__)
app = flask.Flask(__name__)
app.config['JSON_SORT_KEYS'] = False
app.config['JWT_SECRET_KEY'] = 'super-secret'
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = 3600
jwt = JWTManager(app)
CORS(app)
blocklist = set()
@app.route('/api/user/', methods=['GET'])
def user():
    return jsonify({'message': 'User API is working'}),200

#Registration
@app.route('/api/user/register/', methods=['POST'])
@cross_origin()
def register():
    try:
        data = request.get_json()
        id=insert_user(data)
        email=data['email']
        data={'inserted_id': id}
        return jsonify({'message': 'User registered successfully', 'data': data}),200
    except Exception as e:
        logging.error(str(e))
        return jsonify({'message': 'User registration failed','data': str(e)}),400

#verify user, {should this be a patch request?}
@app.route('/api/user/verify/', methods=['POST'])
@cross_origin()
def verify():
    try:
        data = request.get_json()
        if verify_user(data):
            return jsonify({'message': 'User verified successfully'}),200
        return jsonify({'message': 'User verification failed','data': 'Invalid credentials'}),401
    except Exception as e:
        logging.error(str(e))
        return jsonify({'message': 'User verification failed','data': str(e)}),409

#login
@app.route('/api/user/login/', methods=['POST'])
@cross_origin()
def login():
    try:
        data = request.get_json()
        res,bbid=find_user(data)
        if res:
            email=data['email']
            access_token=create_access_token(identity=email)
            data={'access_token':access_token,'userid':bbid,'email':email}
            return jsonify({'message': 'User logged in successfully', 'data':data}),200
        return jsonify({'message': 'User login failed','data': 'Invalid credentials'}),401
    except Exception as e:
        logging.error(str(e))
        return jsonify({'message': 'User login failed','data': str(e)}),400

#password reset code
@app.route('/api/user/pwreset/code', methods=['POST'])
@cross_origin()
def pwreset_code():
    try:
        data = request.get_json()
        if pwrst_code(data):
            return jsonify({'message': 'Password reset code sent successfully'}),200
        return jsonify({'message': 'Password reset code failed','data': 'Invalid credentials'}),401
    except Exception as e:
        logging.error(str(e))
        return jsonify({'message': 'Password reset code failed','data': str(e)}),409

#password reset
@app.route('/api/user/pwreset/', methods=['POST'])
@cross_origin()
def pwreset():
    try:
        data = request.get_json()
        if pwrst(data):
            return jsonify({'message': 'Password reset successful'}),200
        return jsonify({'message': 'Password reset failed','data': 'Invalid credentials'}),401
    except Exception as e:
        logging.error(str(e))
        return jsonify({'message': 'Password reset failed','data': str(e)}),409
#logout
@app.route('/api/user/logout/', methods=['POST'])
@cross_origin()
@jwt_required()
def logout():
    try:
        blocklist.add(get_jwt()['jti'])
        return jsonify({'message': 'User logged out successfully'}),200
    except Exception as e:
        logging.error(str(e))
        return jsonify({'message': 'User logout failed','data': str(e)}),409

@jwt.token_in_blocklist_loader
def check_if_token_in_blocklist(jwt_header, jwt_payload):
    return jwt_payload['jti'] in blocklist

#Protected routes, dummy api to see jwt working
@app.route('/api/user/protected/', methods=['GET'])
@cross_origin()
@jwt_required()
def protected():
    return jsonify({'message': 'User is logged in'}),200

#update user details == update preferences only.

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000,debug=True)