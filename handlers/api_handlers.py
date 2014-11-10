import webapp2

from scripts import get_depts
from models import Department, ROOT_DEPT_KEY
from scripts.google_book_api import get_book_details
import logging

API_VERSION = 1
API_URL = "/api/v%d"

class api_base(webapp2.RequestHandler):
    def get(self):
        self.response.out.write("Welcome to the API Layer!")

class api_helloworld(webapp2.RequestHandler):
    def get(self):
        self.response.out.write("Hello World")

class api_department(webapp2.RequestHandler):
    def get(self):
        query = Department.query(ancestor=ROOT_DEPT_KEY)
        self.response.out.write("<p>These already exist " + str(query.fetch()) +"</p>")
        all_depts = get_depts.get_options()
        
        for abbrev in all_depts:
            dept_exists = query.filter(Department.abbrev == abbrev).count() > 0
            if not dept_exists:
                dept = Department(parent=ROOT_DEPT_KEY, abbrev=abbrev)
                dept.put()
                self.response.out.write("<p>Inserted department " + abbrev +"</p>")
                
                

class api_google_books(webapp2.RequestHandler):
    def post(self):
        isbn = self.request.get('isbn')
        self.response.out.write(get_book_details(isbn))
        
app = webapp2.WSGIApplication([
    (API_URL % (API_VERSION), api_base),
    (API_URL % (API_VERSION) + "/", api_base),
    (API_URL % (API_VERSION) + "/helloworld", api_helloworld),
    (API_URL % (API_VERSION) + "/book_api", api_google_books),
    (API_URL % (API_VERSION) + "/add-departments", api_department),
], debug=True)
