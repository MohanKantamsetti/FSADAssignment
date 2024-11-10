#code to connect to the database.
import os,pymongo
from pymongo import MongoClient
def mongo_connect():
    #check if env variables are set. if not set, connect to local mongo. handle key errors and value errors.
    if os.getenv('DB_SERVICE') is None: 
        try:
            client = MongoClient('localhost', 27017)
            return client
        except pymongo.errors.ServerSelectionTimeoutError as e:
            stderr = "Unable to connect to Repo DB with exception {}".format(str(e))
            raise Exception(stderr)
        except pymongo.errors.OperationFailure as e:
            stderr = 'Authentication failed while connecting to Repo DB -> {}'.format(e)
            raise Exception(stderr)
        except Exception as e:
            stderr = 'Unable to connect to repo with exception {}'.format(str(e))
            raise Exception(stderr)
    else:
        try:
            db_service  = os.getenv('DB_SERVICE')
            db_port     = os.getenv('DB_PORT')
            db_user     = os.getenv('DB_USER')
            db_pass     = os.getenv('DB_PASSWORD')
            db_auth     = os.getenv('DB_NAME')
            print("##########DB Service: ", db_service)
            client      = MongoClient(host=db_service,port=int(db_port),username=db_user,password=db_pass,authSource=db_auth)
            return client

        except pymongo.errors.ServerSelectionTimeoutError as e:
            stderr = "Unable to connect to Repo DB with exception {}".format(str(e))
            raise Exception(stderr)

        except pymongo.errors.OperationFailure as e:
            stderr = 'Authentication failed while connecting to Repo DB -> {}'.format(e)
            raise Exception(stderr)

        except Exception as e:
            stderr = 'Unable to connect to repo with exception {}'.format(str(e))
            raise Exception(stderr)

class dbAccess:
    client = None
    @classmethod
    def get_client_if_none(cls):
        if cls.client is None:
            cls.client = mongo_connect()
    
    def insert_record(cls,db,collection,document):
        try:
            cls.get_client_if_none()
            db = cls.client[db]
            collection = db[collection]
            res=collection.insert_one(document)
            return str(res.inserted_id)
        
        except Exception as e:
            raise Exception(str(e))
        
    def insert_many_records(cls,db,collection,document):
        try:
            #add insert_one and count of records if required.
            cls.get_client_if_none()
            db = cls.client[db]
            collection = db[collection]
            res=collection.insert_many(document)
            return res.inserted_ids
        except Exception as e:
            raise Exception(str(e))

    def find_record(cls,db,collection,query):
        try:
            cls.get_client_if_none()
            db = cls.client[db]
            collection = db[collection]
            res=collection.find_one(query)
            if res is not None:
                res.pop('_id')    #drop the _id field from the result.
            return res
        except Exception as e:
            raise Exception(str(e))
    
    def find_records(cls,db,collection,query):
        try:
            cls.get_client_if_none()
            db = cls.client[db]
            collection = db[collection]
            res=collection.find(query)
            return res
        except Exception as e:
            raise Exception(str(e))
        
    def update_record(cls,db,collection,query,update):
        try:
            cls.get_client_if_none()
            db = cls.client[db]
            collection = db[collection]
            res=collection.update_one(query,{"$set":update})
            return res.modified_count #return the number of records modified.
        except Exception as e:
            raise Exception(str(e))
    
    def delete_record(cls,db,collection,query):
        try:
            cls.get_client_if_none()
            db = cls.client[db]
            collection = db[collection]
            res=collection.delete_one(query)
            return res.deleted_count
        except Exception as e:
            raise Exception(str(e))
    
    def delete_records(cls,db,collection,query):
        try:
            cls.get_client_if_none()
            db = cls.client[db]
            collection = db[collection]
            res=collection.delete_many(query)
            return res
        except Exception as e:
            raise Exception(str(e))
    
    def get_latest_id(cls,db,collection):
        try:
            cls.get_client_if_none()
            db = cls.client[db]
            collection = db[collection]
            res=collection.find().sort('_id',-1).limit(1)
            res=[i for i in res] #convert cursor object to list.
            if len(res)==0:
                return None
            return res[0]
        except Exception as e:
            raise Exception(str(e))