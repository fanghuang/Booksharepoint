
from google.appengine.api import users
from google.appengine.ext.webapp.util import login_required
import webapp2
import logging

from utils import person_utils
import main

### Pages ###

##### Mostly copied and refactored from DiceWithFriends 
class BaseRequestHandler(webapp2.RequestHandler):
    """This is the base handler for all other Request Handlers.
    """
    #This variable stores the jinja2 environment of the templates.
    environment = None

    #This variable will store the name of the file which is the template for this Handler's response HTML page.
    template = None
    
    #This variable will store the wrapper object of the Google user account
    person = None
    
    # This variable will hold the values to render into the template
    values = {}

    def __init__(self, *args):
        """Initializes self.template to the- actual template file in stored in BaseRequestHandler.template"""
        super(BaseRequestHandler, self).__init__(*args)
        if not self.environment:
            self.environment = main.jinja_env
            
        user = users.get_current_user()
        # If not logged in, go to some login page and redirect
        if not user:
            self.template = "templates/index.html"
            self.values = {'login_url': users.create_login_url("/")}
        else:
            self.person = person_utils.get_person_by_email(user.email())
            self.values = {'person': self.person,
                      'cart' : self.person.get_cart(),
                      'logout_url': users.create_logout_url("/")}
            
    def get_template(self):
        return self.environment.get_template(self.template)

    def render(self, non_template=None, **kwargs):
        """Renders a template with the specified keyword arguments."""
        logging.info("["+self.template+"] " + str(kwargs))
        if self.template:
            self.response.out.write(self.get_template().render(**kwargs))
        else:
            self.response.out.write(non_template)
            
    def get(self):
        self.render(**self.values)

    def post(self):
        """By default the post request performs a get unless overridden."""
        self.get()
        
    def update_values(self, person, values):
        raise Exception("Subclasses must override this method")

class BaseUserPageRequestHandler(BaseRequestHandler):
    
    def __init__(self, *args):
        """Initializes self.template to the- actual template file in stored in BaseRequestHandler.template"""
        super(BaseUserPageRequestHandler, self).__init__(*args)
  
    @login_required
    def get(self):
        super(BaseUserPageRequestHandler, self).get()

    def update_values(self, person, values):
        raise Exception("Subclasses must override this method")
  
### Actions ###  

class BaseActionRequestHandler(webapp2.RequestHandler):
    """ALL action handlers should inherit from this one."""
    def __init__(self, *args):
        super(BaseActionRequestHandler, self).__init__(*args)
    
    def get(self):
        """By default the get request performs a post unless overridden."""
        self.post()
        
    def post(self):
        user = users.get_current_user()
        if not user:
            raise Exception("Missing user!")
        person = person_utils.get_person_by_email(user.email())
        self.handle_post(person)
        
    def handle_post(self, person):
        raise Exception("Subclass must implement handle_post!")