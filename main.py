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
import sys
# Third party libraries path must be fixed before importing webapp2
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'includes/external'))

import webapp2
import jinja2

from handlers import main_handlers, action_handlers

jinja_env = jinja2.Environment(
  loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
  autoescape=True)

app = webapp2.WSGIApplication([
    ("/", main_handlers.HomePage),
    ("/search", main_handlers.SearchPage),
    ('/cart', main_handlers.CartPage),
    ('/bookform', main_handlers.BookFormPage),
    ("/insertbook", action_handlers.InsertBookAction),
    ("/deletebook", action_handlers.DeleteBookAction),
    ("/forsale", main_handlers.ForSalePage)
], debug=True)

