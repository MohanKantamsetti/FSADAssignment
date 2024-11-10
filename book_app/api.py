'''
Flask app to handle books api.
'''
import flask, flask_cors, json, os, sys, time
from flask import request, jsonify
from flask_cors import CORS, cross_origin, CORS
from flask_jwt_extended import JWTManager, jwt_required
from models import *
import logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s')
logger=logging.getLogger(__name__)
app = flask.Flask(__name__)
app.config['JSON_SORT_KEYS'] = False
app.config['JWT_SECRET_KEY']='super-secret' #later replace with resources/config.py
CORS(app)
jwt = JWTManager(app)

@app.route('/api/books/', methods=['GET'])
@cross_origin()
@jwt_required()
def books():
    return jsonify({'message': 'Books API is working'}),200

#parameters non unique fields : owner, author, genre, condition, availability, location.
#offset, limit, sort.
@app.route('/api/books', methods=['GET'])
@cross_origin()
@jwt_required()
def get_books():
    try:
        if len(request.args)>4:
            data={
                'Any 1 of the following': 'owner, author, genre, condition, availability, location',
                'Optional': 'offset, limit, sort'
            }
            return jsonify({'message': 'Invalid query parameters','data':data}), 400
        res=get_books_bl(request.args)
        if len(res)==0:
            return jsonify({'message': 'Books not found'}), 404
        return jsonify({'message': 'Books fetched successfully','data':res}), 200
    except Exception as e:
        logger.error(str(e))
        return jsonify({'message': str(e)}), 500


@app.route('/api/books/', methods=['POST'])
@cross_origin()
@jwt_required()
def create_book():
    try:
        data = request.get_json()
        res=create_book_bl(data)
        return jsonify({'message': 'Book created successfully','data':res}), 201
    except Exception as e:
        logger.error(str(e))
        return jsonify({'message': str(e)}), 500

@app.route('/api/books/', methods=['PATCH'])
@cross_origin()
@jwt_required()
def update_book():
    try:
        data = request.get_json()
        if update_book_bl(data):
            return jsonify({'message': 'Book updated successfully'}), 200
        else:
            return jsonify({'message': 'Failed to update book'}), 500
    except Exception as e:
        logger.error(str(e))
        return jsonify({'message': str(e)}), 500
    
@app.route('/api/books/<bid>', methods=['GET'])
@cross_origin()
@jwt_required()
def get_book_by_id(bid):
    try:
        res=get_book_by_id_bl(bid)
        if res is None:
            return jsonify({'message': 'Book not found'}), 404
        return jsonify({'message': 'Book fetched successfully','data':res}), 200
    except Exception as e:
        logger.error(str(e))
        return jsonify({'message': str(e)}), 500

@app.route('/api/books/query', methods=['POST'])
@cross_origin()
@jwt_required()
def get_books_by_query():
    try:
        data = request.get_json()
        res=get_books_by_query_bl(data)
        if len(res)==0:
            return jsonify({'message': 'Books not found'}), 404
        return jsonify({'message': 'Books fetched successfully','data':res}), 200
    except Exception as e:
        logger.error(str(e))
        return jsonify({'message': str(e)}), 500
    
#delete book by id
@app.route('/api/books/<bid>', methods=['DELETE'])
@cross_origin()
@jwt_required()
def delete_book_by_id(bid):
    try:
        if delete_book_by_id_bl(bid):
            return jsonify({'message': 'Book deleted successfully'}), 200
        else:
            return jsonify({'message': 'Failed to delete book'}), 500
    except Exception as e:
        logger.error(str(e))
        return jsonify({'message': str(e)}), 500
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)