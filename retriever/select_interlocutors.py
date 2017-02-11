import facebook
import sys
from api_utils import read_token, pull_contact_list, pull_messages, find_contact


# PARAMETERS
INBOX_LIMIT = 10

class Person:
    def __init__(self, id, username, firstname=None, lastname=None, gender=None):
        self.id = id
        self.first_name = firstname
        self.last_name = lastname
        self.username = username
        self.gender = gender

    def details(self):
        print("I am " + self.username, end=". ")
        if self.first_name and self.last_name and self.gender:
            print("I am a " + self.gender + " and my real name is " + \
                    self.first_name + " " + self.last_name)
        else:
            print("I am your interlocutor.")


def get_contact_list(options, inbox, user):
    partners = []
    contacts = pull_contact_list(inbox['inbox'], user.id, loop_limit=options.l)
    for contact in contacts:
        partners.append(Person(contacts[contact]['id'], contacts[contact]['name']))
    return partners

def select_contact(options, inbox, user):
    if options.contact:
        interlocutor = find_contact(inbox['inbox'], user.id, options.contact)
        partner = Person(interlocutor['id'], interlocutor['name'])
    else:
        print("Retrieving last recent contacts...")
        contacts = pull_contact_list(inbox['inbox'], user.id, loop_limit=options.l)
        for contact in contacts:
            print(contact, contacts[contact]['name'])
        print("Enter the contact number you want to stalk your conversation with:")
        target = int(input())
        if options.debug:
            print(contacts[target])
        selected = contacts[target]['name']
        partner = Person(contacts[target]['id'], contacts[target]['name'])
        print(selected + " selected")
    return partner


def select_interlocutors(options):
    graph = None
    try:
        graph = facebook.GraphAPI(access_token=read_token(), version='2.3')
        identity = graph.get_object(id="me")
    except facebook.GraphAPIError as e:
        print('Something went wrong:', e.type, e.message)
        sys.exit(1)

    user = Person(identity['id'], identity['name'],
            firstname=identity['first_name'], lastname=identity['last_name'],
            gender=identity['gender'])
    if options.debug:
        user.details()

    inbox = None
    try:
        inbox = graph.get_object(id=user.id, fields="inbox{to, comments}")
    except facebook.GraphAPIError as e:
        print('Something went wrong:', e.type, e.message)
        sys.exit(1)

    if options.all:
        partners = get_contact_list(options, inbox, user)
    else:
        partner = select_contact(options, inbox, user)
        partners = [partner]

    if options.debug:
        for dude in partners:
            dude.details()

    return user, partners, inbox['inbox']
