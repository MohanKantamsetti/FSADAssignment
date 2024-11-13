#code to perform crud operations on the database of books.
from resources.dbcon import dbAccess
from book_app.models import Book
db=dbAccess()
import logging

def insert_bookdb(book):
    data=book.to_dict()
    try:
        res=db.insert_record('bookbarter','books',data)
        return res #return the id of the inserted record.
    except Exception as e:
        logging.error(str(e.message))
        raise Exception(str(e))

def get_bid():
    res=db.get_latest_id('bookbarter','books')
    if res is None:
        return 1
    bid=res['bid']
    return int(bid[1:])+1
    
def update_bookdb(query,book):
    data=book.to_dict()
    try:
        res=db.update_record('bookbarter','books',query,data)
        if res==1:
            return True
        else:
            return False
    except Exception as e:
        raise Exception(str(e))
    
def get_bookbyid_db(bid):
    try:
        query={'bid':bid}
        res=db.find_record('bookbarter','books',query)
        return res
    except Exception as e:
        raise Exception(str(e))

def get_books_query_db(query,limit=None,offset=None,sort=None):
    try:
        res=db.find_records('bookbarter','books',query)
        #first sort, then offset, then limit.
        if sort is not None:
            res=res.sort(sort)
        if offset is not None:
            res=res.skip(offset)
        if limit is not None:
            res=res.limit(limit)
        books=[]
        for r in res:
            r.pop('_id')
            books.append(Book(r))
        return books
    except Exception as e:
        raise Exception(str(e))

def delete_book_by_id_db(query):
    try:
        res=db.delete_record('bookbarter','books',query)
        if res==1:
            return True
        else:
            return False
    except Exception as e:
        raise Exception(str(e))