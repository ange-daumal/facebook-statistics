from main import init_user
from optparse import OptionParser

parser = OptionParser()
parser.add_option("-l", "--list-contact", type="int", dest="n", default=1,
        help="list n * 18 contacts", metavar="NUMBER")
parser.add_option("-c", "--contact", type="string", dest="contact", action="store",
        help="specify a contact to stalk the conversation with", metavar="STRING")
'''
parser.add_option("-l", "--list", type="choice", dest="category", action="store",
        default="animals", choices=["animals", "expression"],
        help="choose a sentence category to generate", metavar="STRING")
'''
parser.add_option("-d", "--debug", dest="debug", action="store_true",
        help="print debug messages", metavar="BOOLEAN")
(options, args) = parser.parse_args()

if __name__ == "__main__":
    init_user(options)
