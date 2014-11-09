import webapp2
from google.appengine.ext import ndb

from scripts import get_depts
from models import Department, ROOT_DEPT_KEY

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
    	dept = Department.query(ancestor=ROOT_DEPT_KEY).fetch()
    	for option in get_depts.get_options():
    		if option not in dept:
	    		dept = Department(abbrev=option,parent=ROOT_DEPT_KEY)
	    		dept.put()
        

app = webapp2.WSGIApplication([
    (API_URL % (API_VERSION), api_base),
    (API_URL % (API_VERSION) + "/", api_base),
    (API_URL % (API_VERSION) + "/add-department", api_department),
    (API_URL % (API_VERSION)+ "/helloworld", api_helloworld)
], debug=True)