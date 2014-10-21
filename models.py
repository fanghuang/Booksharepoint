from google.appengine.ext import ndb

class WeatherPics(ndb.Model):
    image_url = ndb.StringProperty()
    caption = ndb.StringProperty()
    last_touch_date_time = ndb.DateTimeProperty(auto_now=True)
    