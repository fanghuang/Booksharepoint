import webapp2

API_VERSION = 1
API_URL = "/api/v%d/" % API_VERSION

class api_base(webapp2.RequestHandler):
    def get(self):
        self.response.out.write("Welcome to the API Layer!")

class api_helloworld(webapp2.RequestHandler):
    def get(self):
        self.response.out.write("Hello World")

app = webapp2.WSGIApplication([
    (API_URL, api_base),
    (API_URL + "helloworld", api_helloworld)
], debug=True)