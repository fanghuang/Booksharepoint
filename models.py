from google.appengine.ext import ndb

ROOT_DEPT_KEY = ndb.Key("Entity", "root_dept")

# TODO: Delete this and rename to model.py
PARENT_KEY = ndb.Key("Entity", "root_weatherpics")
class WeatherPics(ndb.Model):
    image_url = ndb.StringProperty()
    caption = ndb.StringProperty()
    last_touch_date_time = ndb.DateTimeProperty(auto_now=True)
    
class Department(ndb.Model):
    full_name = ndb.StringProperty()
    abbrev = ndb.StringProperty()
    
class Person(ndb.Model):
	# account = ndb.UserProperty()
    display_name = ndb.StringProperty()
    contact_info = ndb.StringProperty()
    
    def get_name(self):
        """ Returns the best name available for a Person """
        if self.display_name:
            return self.display_name
        return self.key.string_id()  # Email address

class Book(ndb.Model):
    seller = ndb.KeyProperty(kind=Person)
    cart_key = ndb.KeyProperty(kind=Person)
    
    price = ndb.FloatProperty()
    
    isbn = ndb.StringProperty() # unique
    author = ndb.StringProperty()
    title = ndb.StringProperty()
    img_url = ndb.StringProperty()
    
    dept = ndb.KeyProperty(kind=Department)
    
    comments = ndb.TextProperty()
    
    last_touch_date_time = ndb.DateTimeProperty(auto_now=True)