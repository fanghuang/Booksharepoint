from google.appengine.ext import ndb

from base_handlers import BaseActionRequestHandler
from models import Book, ROOT_BOOK_KEY
import logging
import json

class InsertBookAction(BaseActionRequestHandler):
    def post(self):
        entity_key_urlsafe = self.request.get("entity_key")
        book = None
        
        book_seller_key = self.person.key        
        # Make sure POST request is given these names
        book_image_url = self.request.get("image-url")
        book_price = float(self.request.get("price"))    
        book_isbn = self.request.get("isbn")
        book_author = self.request.get("author")
        book_title = self.request.get("title")
        book_dept = self.request.get("dept-abbrev")
        book_condition_id = int(self.request.get("condition"))
        
        if entity_key_urlsafe:
            book_key = ndb.Key(urlsafe=entity_key_urlsafe)
            book = book_key.get()
            
            # keep same seller key
            # don't need cart_key
            
            book.price = book_price
            
            if book_isbn:
                book.isbn = book_isbn
            if book_author:
                book.author = book_author
            if book_title:
                book.title = book_title
            if book_dept:
                book.dept = book_dept.lower()
            if book_condition_id:
                book.condition_id = book_condition_id

            book.image_url = book_image_url
        else:
            book = Book(parent=ROOT_BOOK_KEY, seller_key = book_seller_key, price=book_price,
                        image_url=book_image_url)
            if book_isbn:
                book.isbn = book_isbn
            if book_author:
                book.author = book_author
            if book_title:
                book.title = book_title
            if book_dept:
                book.dept = book_dept.lower()
            if book_condition_id:
                book.condition_id = book_condition_id

            # TODO: Replace above with this when all fields are given
#             book = Book(parent=ROOT_BOOK_KEY, seller_key = book_seller_key, price=book_price, 
#                         image_url=book_image_url, 
#                         isbn = book_isbn, author = book_author, title = book_title, 
#                         dept = book_dept, comments = str(book_comments).strip())
        logging.info("Adding Book: " + str(book))
        book.put()
        self.redirect(self.request.referer)
        

class DeleteBookAction(BaseActionRequestHandler):
    def post(self):
        book_key = ndb.Key(urlsafe=self.request.get("entity_key"))
        book_key.delete()
        self.redirect(self.request.referer)
        
class AddToCartAction(BaseActionRequestHandler):
    def post(self):
        entity_key_urlsafe = self.request.get("entity_key")
        
        resp = None
        if entity_key_urlsafe:
            book_key = ndb.Key(urlsafe=entity_key_urlsafe)
            book = book_key.get()
            if book.cart_key:
                # Already in someone's cart
                resp = {"status" : "Error", "code" : "InCart", "message" : "This book has already been added to someone else's cart"}
            else:
                book.cart_key = self.person.key
                book.put()
                resp = {"status" : "Success", "code" : "OK", "message" : "Book added to cart"}
        else:
            resp = {"status" : "Error", "code" : "NoKey", "message" : "No key was given to the method"}
        
        if resp:
            self.response.out.write(json.dumps(resp))
            
class RemoveFromCartAction(BaseActionRequestHandler):
    def post(self):
        entity_key_urlsafe = self.request.get("entity_key")
         
        if entity_key_urlsafe:
            book_key = ndb.Key(urlsafe=entity_key_urlsafe)
            book = book_key.get()
            book.cart_key = None
            book.put()
         
        