
from google.appengine.api import users
import webapp2

import main
from utils import person_utils
from google.appengine.ext.webapp.util import login_required

### Pages ###

class BaseRequestHandler(webapp2.RequestHandler):
    """This is the base handler for all other Request Handlers.
    """
    #This variable stores the jinja2 environment of the templates.
    environment = None

    #This variable will store the name of the file which is the template for this Handler's response HTML page.
    template = None

    def __init__(self, *args):
        """Initializes self.template to the- actual template file in stored in BaseRequestHandler.template"""
        super(BaseRequestHandler, self).__init__(*args)
        if not self.environment:
            self.environment = main.jinja_env
            
    def get_template(self):
        return self.environment.get_template(self.template)

    def render(self, non_template=None, **kwargs):
        """Renders a template with the specified keyword arguments."""
        if self.template:
            self.response.out.write(self.get_template().render(**kwargs))
        else:
            self.response.out.write(non_template)
            
    def get(self):
        self.render()

    def post(self):
        """By default the post request performs a get unless overridden."""
        self.get()

##### Mostly copied and refactored from DiceWithFriends 
class BaseUserPageRequestHandler(BaseRequestHandler):
    
    person = None
    
    def __init__(self, *args):
        """Initializes self.template to the- actual template file in stored in BaseRequestHandler.template"""
        super(BaseUserPageRequestHandler, self).__init__(*args)
  
    @login_required
    def get(self):
        env = main.jinja_env
        user = users.get_current_user()
        values = {}
        # If not logged in, go to some login page and redirect
        if not user:
            self.template = env.get_template("templates/index.html")
            values = {'login_url': users.create_login_url(self.request.referer)}
        else:
            self.person = person_utils.get_person_from_email(user.email())
            values = {'person': self.person,
                      'logout_url': users.create_logout_url("/")}
#             self.update_values(player, values)
        self.render(**values)

    def update_values(self, person, values):
        raise Exception("Subclasses must override this method")

