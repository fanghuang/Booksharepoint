from google.appengine.ext import ndb

from base_handlers import BaseActionRequestHandler
from models import Book, ROOT_BOOK_KEY

class InsertBookAction(BaseActionRequestHandler):
    def post(self):
        entity_key_urlsafe = self.request.get("entity_key")
        
        book = None

        if entity_key_urlsafe:
            book_key = ndb.Key(urlsafe=entity_key_urlsafe)
            book = book_key.get()
            # TODO: Change this to isbn
            book.image_url = self.request.get("image-url")
            # TODO: Change this to price
            book.price = float(self.request.get("caption"))
        else:
            # TODO: Make this actually a book object
            book = Book(seller_key = self.person.key, 
                                    parent=ROOT_BOOK_KEY,
                                    image_url=self.request.get("image-url"),
                                    price=float(self.request.get("caption")))
        book.put()
        self.redirect(self.request.referer)
        

class DeleteBookAction(BaseActionRequestHandler):
    def post(self):
        book_key = ndb.Key(urlsafe=self.request.get("entity_key"))
        book_key.delete()
        self.redirect(self.request.referer)
        