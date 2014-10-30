from base_handlers import BaseRequestHandler, BaseUserPageRequestHandler

# TODO: Delete this
from models import WeatherPics, PARENT_KEY
class WeatherPicsPage(BaseRequestHandler):
    template = "templates/main.html"
    
    def get(self):
        weatherpics_query = WeatherPics.query(ancestor=PARENT_KEY).order(-WeatherPics.last_touch_date_time)
        values = {"weatherpics_query": weatherpics_query}
        self.render(**values)

class HomePage(BaseRequestHandler):
    template = 'templates/index.html'

# TODO: Change this to modals    
class BookFormPage(BaseRequestHandler):
    template = 'templates/book_form.html'

""" BaseUserPageRequestHandler = must be logged in to view """
   
class CartPage(BaseUserPageRequestHandler):
    template = 'templates/cart.html'