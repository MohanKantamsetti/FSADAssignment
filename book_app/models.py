'''
Book class and business logic.
'''
import logging,sys,os
sys.path.append(os.path.abspath(os.path.join('../')))
from resources.book_crud import *

class Book:
    def __init__(self, data):
        self.owner          = data['owner']         # This is the user who created/owns the book
        self.bid            = data['bid']           # This is the unique identifier for the book
        self.title          = data['title']
        self.author         = data['author']
        self.genre          = data['genre']
        self.isbn           = data['isbn']          #https://isbnsearch.org/isbn/{isbn}
        self.condition      = data['condition']
        self.availability   = data['availability']
        self.location       = data['location']      # This is the location of the book
        self.description    = data['description']   
    
    def to_dict(self):
        return {
            'owner': self.owner,
            'bid': self.bid,
            'title': self.title,
            'author': self.author,
            'genre': self.genre,
            'isbn': self.isbn,
            'condition': self.condition,
            'availability': self.availability,
            'location': self.location,
            'description': self.description
        }

def create_book_bl(data):
    try:
        data['bid'] = 'b'+str(get_bid())
        book=Book(data)
        #validate if the userid is valid/exists.
        res=insert_bookdb(book)
        return res
    except Exception as e:
        logging.error(str(e))
        return 'Failed to create book'
    
def update_book_bl(data):
    try:
        book=Book(data)
        query={'bid':book.bid}
        return update_bookdb(query,book)
    except Exception as e:
        logging.error(str(e))
        return 'Failed to update book'

#bid, isbn are unique fields.
def get_book_by_id_bl(bid):
    try:
        return get_bookbyid_db(bid)
    except Exception as e:
        logging.error(str(e))
        return 'Failed to get book'

'''
#add regex to match partial strings.
title, author, genre condition, location, description
'''    
def get_books_by_query_bl(query):
    try:
        for key in query:
            if key in ['bid','isbn','owner','availability']:
                continue
            query[key]={'$regex':query[key], '$options': 'i'}
        #if multiple queries are present, then use $or operator.
        if len(query)>1:
            query=[{k:v} for k,v in query.items()]
            query={'$or': query}
        logging.debug(query)
        books=[]
        for book in get_books_query_db(query):
            books.append(book.to_dict())
        return books
    except Exception as e:
        logging.error(str(e))
        return 'Failed to get books'
    
def delete_book_by_id_bl(bid):
    try:
        query={'bid':bid}
        return delete_book_by_id_db(query)
    except Exception as e:
        logging.error(str(e))
        return 'Failed to delete book'
    
def get_books_bl(args):
    query={}
    limit=None
    offset=None
    sort=None
    for key in args:
        if key in ['limit','sort','page']:
            if key=='page':
                offset=int(args['page'])*int(args['limit'])
            elif key=='limit':
                limit=int(args[key])
            elif key=='sort':
                sort=args[key]
            continue
        query[key]=args[key]
    books=[]
    try:
        for book in get_books_query_db(query,limit,offset,sort):
            books.append(book.to_dict())
        return books
    except Exception as e:
        logging.error(str(e))
        return 'Failed to get books'