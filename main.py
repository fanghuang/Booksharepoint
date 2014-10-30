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

from handlers import main_handlers

from models import WeatherPics, PARENT_KEY

jinja_env = jinja2.Environment(
  loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
  autoescape=True)
        
class InsertBookAction(webapp2.RequestHandler):
    def post(self):
        entity_key_urlsafe = self.request.get("entity_key")
        
        book = None
        if entity_key_urlsafe:
            book_key = ndb.Key(urlsafe=entity_key_urlsafe)
            book = book_key.get()
            # TODO: Change this to isbn
            book.image_url = self.request.get("image-url")
            # TODO: Change this to price
            book.caption = self.request.get("caption")
        else:
            # TODO: Make this actually a book object
            book = WeatherPics(parent=PARENT_KEY,
                                    image_url=self.request.get("image-url"),
                                    caption=self.request.get("caption"))
        book.put()
        self.redirect(self.request.referer)

class DeleteBookAction(webapp2.RequestHandler):
    def post(self):
        book_key = ndb.Key(urlsafe=self.request.get("entity_key"))
        book_key.delete()
        self.redirect(self.request.referer)
        

app = webapp2.WSGIApplication([
    ("/", main_handlers.HomePage),
    ('/cart', main_handlers.CartPage),
    ('/bookform', main_handlers.BookFormPage),
    ("/insertbook", InsertBookAction),
    ("/deletebook", DeleteBookAction),
], debug=True)

