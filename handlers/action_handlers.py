from google.appengine.ext import ndb

from base_handlers import BaseActionRequestHandler
from models import Book, ROOT_BOOK_KEY
import logging

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
        
        if entity_key_urlsafe:
            book_key = ndb.Key(urlsafe=entity_key_urlsafe)
            book = book_key.get()
            
            # keep same seller key
            # don't need cart_key
            
            book.price = book_price
            
            # TODO: Uncomment these when all fields are given
#             book.isbn = book_isbn
#             book.author = book_author
#             book.title = book_title
            if book_dept:
                book.dept = book_dept
#             book.comments = book_comments
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
         
        if entity_key_urlsafe:
            book_key = ndb.Key(urlsafe=entity_key_urlsafe)
            book = book_key.get()
            book.cart_key = self.person.key
            book.put()
            
        self.redirect(self.request.referer)
         
        