import webapp2
from scripts.google_book_api import get_book_details

API_VERSION = 1
API_URL = "/api/v%d"

class api_base(webapp2.RequestHandler):
    def get(self):
        self.response.out.write("Welcome to the API Layer!")

class api_helloworld(webapp2.RequestHandler):
    def get(self):
        self.response.out.write("Hello World")
        
class api_google_books(webapp2.RequestHandler):
    def post(self):
        isbn = self.request.get('isbn')
        self.response.out.write(get_book_details(isbn))

app = webapp2.WSGIApplication([
    (API_URL % (API_VERSION), api_base),
    (API_URL % (API_VERSION) + "/", api_base),
    (API_URL % (API_VERSION) + "/book_api", api_google_books),
    (API_URL % (API_VERSION)+ "/helloworld", api_helloworld)
], debug=True)