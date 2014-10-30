from models import Person
import logging
from google.appengine.ext import ndb

def get_person_from_email(email):
    """Helper method to get the Player object corresponding to the given User.
    Creates a new Player object if one didn't exist already.
    """
    email = email.lower()
    person = Person.get_by_id(email, parent=get_parent_key_from_email(email))
    logging.info("person = " + str(person)) 
    if not person:
        logging.info("Failed to find person by id, creating new user")
        # DONE: Create a new person with the id = email and parent of get_parent_key_from_email
        person = Person(parent=get_parent_key_from_email(email),
                    id=email)
        person.put()
    return person

def get_parent_key(user):
    return get_parent_key_from_email(user.email())

def get_parent_key_from_email(email):
    return ndb.Key("Entity", email.lower())
