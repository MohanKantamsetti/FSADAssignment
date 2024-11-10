#code to perform CRUD operations on the database of users.
from resources.dbcon import dbAccess
from user_app.models import User
db=dbAccess()
def insert_userdb(User):
    data=User.to_dict()
    try:
        res=db.insert_record('bookbarter','users',data)
        return res #return the id of the inserted record.
    except Exception as e:
        raise Exception(str(e))

def get_id():
    res=db.get_latest_id('bookbarter','users')
    if res is None:
        return 1
    bbid=res['bbid']
    return int(bbid[2:])+1

def update_userdb(query,data):
    try:
        res=db.update_record('bookbarter','users',query,data)
        return res #return the number of records updated.
    except Exception as e:
        raise Exception(str(e))

def find_userdb(query):
    try:
        res=db.find_record('bookbarter','users',query)
        if res is None:
            return None
        return User(res)
    except Exception as e:
        raise Exception(str(e))