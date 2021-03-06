from base_handlers import BaseRequestHandler, BaseUserPageRequestHandler

from models import Book, ROOT_BOOK_KEY, Department, ROOT_DEPT_KEY
from google.appengine.ext import ndb

class HomePage(BaseRequestHandler):
    template = "templates/index.html"
    
    def get(self):
        
        # Get all the displayable books
        books_query = Book.query(ancestor=ROOT_BOOK_KEY)  
        # Get the books currently in the cart
        cart_query = []
        
        # check for a person and filter the books
        if self.person:
            books_query = books_query.filter(ndb.OR(Book.cart_key == None, Book.cart_key == self.person.key))
            cart_query = self.person.get_cart()
        else:
            # remove all the books that are in someone's cart
            books_query = books_query.filter(Book.cart_key == None)    
        books_query = books_query.order(-Book.last_touch_date_time)
        
        # Get additional details needed to populate lists
        dept_query = Department.query(ancestor=ROOT_DEPT_KEY).order(Department.abbrev)
        book_conditions = Book.get_conditions()
        
        self.values.update({"books_query": books_query,
                            "cart_query" : cart_query,
                            "dept_query": dept_query, 
                            "book_conditions": book_conditions})        
        self.render(**self.values)
        
class SearchPage(BaseRequestHandler):
    template = "templates/index.html"
    
    def get(self):
        books_query = Book.query(ancestor=ROOT_BOOK_KEY).order(-Book.last_touch_date_time)
        
        # Get additional details needed to populate lists
        dept_query = Department.query(ancestor=ROOT_DEPT_KEY).order(Department.abbrev)
        book_conditions = Book.get_conditions()

        # Perform the search from the "q"uery param
        q = self.request.get("q")
        if q:
            q = q.lower()
            books_query = books_query.filter(ndb.OR(Book.title_lower == q,
                                Book.dept == q, 
                                Book.author_lower == q, 
                                Book.isbn == q))

        self.values.update({"books_query": books_query,
                            "dept_query": dept_query, 
                            "book_conditions": book_conditions})        
        self.render(**self.values)

# TODO: Change this to modals    
class BookFormPage(BaseRequestHandler):
    template = 'templates/book_form.html'

""" BaseUserPageRequestHandler = must be logged in to view """
   
class CartPage(BaseUserPageRequestHandler):
    template = 'templates/cart.html'
    
    def get(self):
        books_query = self.person.get_cart()
        total_cost = 0
        for book in books_query:
            total_cost += book.price
        self.values.update({"books_query": books_query, 
                            "total_cost": "${0:.2f}".format(round(total_cost,2))})
        self.render(**self.values)


class ForSalePage(BaseUserPageRequestHandler):
    template = 'templates/forsale.html'

    def get(self):
        books_query = self.person.get_books_for_sale()
        dept_query = Department.query(ancestor=ROOT_DEPT_KEY).order(Department.abbrev)
        book_conditions = Book.get_conditions()
        self.values.update({"books_query": books_query,
                            "dept_query": dept_query, 
                            "book_conditions": book_conditions})           
        self.render(**self.values)

