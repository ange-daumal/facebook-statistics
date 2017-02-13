import time
from select_interlocutors import select_interlocutors, get_contact_list
from sqlite import fill_database
from optparse import OptionParser


parser = OptionParser()

parser.add_option("-l", "--list-contact", type="int", dest="l", default=1,
        help="list l * 18 contacts", metavar="NUMBER")

parser.add_option("-n", "--messages-number", type="int", dest="n", default=1,
        help="list n * 23 messages", metavar="NUMBER")

parser.add_option("-c", "--contact", type="string", dest="contact",
        action="store",
        help="specify a contact to stalk the conversation with",
        metavar="STRING")

parser.add_option("-a", "--all", dest="all", action="store_true",
        help="do not specify a contact, fill database with all of them",
        metavar="BOOLEAN")

parser.add_option("-r", "--reset", dest="reset", action="store_true",
        help="reset database", metavar="BOOLEAN")

parser.add_option("-d", "--debug", dest="debug", action="store_true",
        help="print debug messages", metavar="BOOLEAN")

(options, args) = parser.parse_args()

if __name__ == "__main__":
    user, partners, inbox = select_interlocutors(options)
    for partner in partners:
        if options.debug:
            print("*** Handling %s" % partner.username)
        fill_database(options, user, partner, inbox)
        time.sleep(20)
