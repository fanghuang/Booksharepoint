from google.appengine.ext import ndb

ROOT_DEPT_KEY = ndb.Key("Entity", "root_dept")
ROOT_BOOK_KEY = ndb.Key("Entity", "root_book")

class Department(ndb.Model):
    full_name = ndb.StringProperty()
    abbrev = ndb.StringProperty()
    
class Person(ndb.Model):
    display_name = ndb.StringProperty()
    contact_info = ndb.StringProperty()
    
    def get_name(self):
        """ Returns the best name available for a Person """
        if self.display_name:
            return self.display_name
        return self.key.string_id()  # Email address
    
    def get_cart(self):
        return Book.query(Book.cart_key == self.key).fetch()
    
    def get_books_for_sale(self):
        return Book.query(Book.seller_key == self.key).fetch()

class Book(ndb.Model):
    seller_key = ndb.KeyProperty(kind=Person)
    cart_key = ndb.KeyProperty(kind=Person)
    
    price = ndb.FloatProperty()
    
    isbn = ndb.StringProperty() 
    author = ndb.StringProperty()
    title = ndb.StringProperty()
    image_url = ndb.StringProperty()
    
    dept = ndb.KeyProperty(kind=Department)
    
    comments = ndb.TextProperty()
    
    last_touch_date_time = ndb.DateTimeProperty(auto_now=True)

    def get_price(self):
        return "${0:.0f}".format(round(self.price,0))