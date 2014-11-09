from models import Person
import logging
from google.appengine.ext import ndb

# def get_person_by_user(user):
#     return get_person_by_email(user.email().lower())

def get_person_by_email(email):
    """Helper method to get the Person object corresponding to the given email.
    Creates a new Person object if one didn't exist already.
    """
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
