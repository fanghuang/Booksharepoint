#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import os
import logging

from google.appengine.ext import ndb
import jinja2
import webapp2

from models import WeatherPics


jinja_env = jinja2.Environment(
  loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
  autoescape=True)

PARENT_KEY = ndb.Key("Entity", "root_weatherpics")

class WeatherPicsPage(webapp2.RequestHandler):
    def get(self):
        weatherpics_query = WeatherPics.query(ancestor=PARENT_KEY).order(-WeatherPics.last_touch_date_time)
        template = jinja_env.get_template("templates/main.html")
        self.response.out.write(template.render({"weatherpics_query": weatherpics_query}))
        
class InsertPicAction(webapp2.RequestHandler):
    def post(self):
        entity_key_urlsafe = self.request.get("entity_key")
        
        if entity_key_urlsafe:
            weatherpic_key = ndb.Key(urlsafe=entity_key_urlsafe)
            weatherpic = weatherpic_key.get()
            weatherpic.image_url = self.request.get("image-url")
            weatherpic.caption = self.request.get("caption")
            weatherpic.put()
        else:
            new_weatherpic = WeatherPics(parent=PARENT_KEY,
                                    image_url=self.request.get("image-url"),
                                    caption=self.request.get("caption"))
            new_weatherpic.put()
        
        self.redirect(self.request.referer)
        
class DeletePicAction(webapp2.RequestHandler):
    def post(self):
        weatherpic_key = ndb.Key(urlsafe=self.request.get("entity_key"))
        weatherpic_key.delete()
        self.redirect(self.request.referer)

class InsertBookCover(webapp2.RequestHandler):
    def post(self):
        entity_key_urlsafe = self.request.get("entity_key")
        
        if entity_key_urlsafe:
            weatherpic_key = ndb.Key(urlsafe=entity_key_urlsafe)
            weatherpic = weatherpic_key.get()
            weatherpic.image_url = self.request.get("image-url")
            weatherpic.caption = self.request.get("caption")
            weatherpic.put()
        else:
            new_weatherpic = WeatherPics(parent=PARENT_KEY,
                                    image_url=self.request.get("image-url"),
                                    caption=self.request.get("caption"))
            new_weatherpic.put()
        self.redirect(self.request.referer)
        

app = webapp2.WSGIApplication([
    ("/", WeatherPicsPage),
    ("/insertpic", InsertPicAction),
    ("/deletepic", DeletePicAction)
], debug=True)

