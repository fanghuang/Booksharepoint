from base_handlers import BaseRequestHandler, BaseUserPageRequestHandler

# TODO: Delete this
from models import WeatherPics, PARENT_KEY
class HomePage(BaseRequestHandler):
    template = "templates/index.html"
    
    def get(self):
        # TODO: Make this query books instead
        books_query = WeatherPics.query(ancestor=PARENT_KEY).order(-WeatherPics.last_touch_date_time)
        self.values.update({"weatherpics_query": books_query})
        self.render(**self.values)

# TODO: Change this to modals    
class BookFormPage(BaseRequestHandler):
    template = 'templates/book_form.html'

""" BaseUserPageRequestHandler = must be logged in to view """
   
class CartPage(BaseUserPageRequestHandler):
    template = 'templates/cart.html'