import webapp2

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
        query the python 

app = webapp2.WSGIApplication([
    (API_URL % (API_VERSION), api_base),
    (API_URL % (API_VERSION) + "/", api_base),
    (API_URL % (API_VERSION) + "/add-department", api_department),
    (API_URL % (API_VERSION)+ "/helloworld", api_helloworld)
], debug=True)