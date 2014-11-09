from base_handlers import BaseRequestHandler, BaseUserPageRequestHandler

from models import Book, ROOT_BOOK_KEY

class HomePage(BaseRequestHandler):
    template = "templates/index.html"
    
    def get(self):
        # TODO: Make this query books instead
        books_query = Book.query(ancestor=ROOT_BOOK_KEY).order(-Book.last_touch_date_time)
        self.values.update({"books_query": books_query})        
        self.render(**self.values)

# TODO: Change this to modals    
class BookFormPage(BaseRequestHandler):
    template = 'templates/book_form.html'

""" BaseUserPageRequestHandler = must be logged in to view """
   
class CartPage(BaseUserPageRequestHandler):
    template = 'templates/cart.html'


class ForSalePage(BaseUserPageRequestHandler):
    template = 'templates/forsale.html'