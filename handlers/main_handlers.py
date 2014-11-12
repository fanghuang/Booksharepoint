from base_handlers import BaseRequestHandler, BaseUserPageRequestHandler

from models import Book, ROOT_BOOK_KEY, Department, ROOT_DEPT_KEY

class HomePage(BaseRequestHandler):
    template = "templates/index.html"
    
    def get(self):
        books_query = Book.query(ancestor=ROOT_BOOK_KEY).order(-Book.last_touch_date_time)

        dept_query = Department.query(ancestor=ROOT_DEPT_KEY).order(Department.abbrev)
        book_conditions = Book.get_conditions()
        self.values.update({"books_query": books_query,
                            "dept_query": dept_query, 
                            "book_conditions": book_conditions})        
        self.render(**self.values)
        
class SearchPage(BaseRequestHandler):
    template = "templates/index.html"
    
    def get(self):
        books_query = Book.query(ancestor=ROOT_BOOK_KEY).order(-Book.last_touch_date_time)
        dept_query = Department.query(ancestor=ROOT_DEPT_KEY).order(Department.abbrev)
        book_conditions = Book.get_conditions()

        q = self.request.get("q")
        dept_param = self.request.get("dept")
        title_param = self.request.get("title")
        isbn_param = self.request.get("isbn")
        
        if q or dept_param or title_param or isbn_param:
            if dept_param:
                books_query = books_query.filter(Book.dept == dept_param.lower())
        
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
        self.values.update({"books_query": books_query})        
        self.render(**self.values)

