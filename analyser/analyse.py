import sqlite3 as lite
import sys
from messages_ratio import compare_words

def get_interlocutors_id(options, cursor):
    if options.contact:
        return cursor.execute("SELECT id, name FROM Interlocutors \
                WHERE name='%s'" % options.contact)
    contacts = []
    tuples = cursor.execute("SELECT id, name FROM Interlocutors")
    for contact in tuples:
        contacts.append(contact)
    # This is weird but I don't know why my "tuples" object just do not last.
    return contacts

def update_ratios(options, cursor):
    contacts = get_interlocutors_id(options, cursor)
    compare_words(options, cursor, contacts)

def print_top(string, cursor, cmd, limit=5):
    print(string)
    for result in cursor.execute(cmd + " LIMIT %d;" % limit):
        print(result)
    print()

def print_result(cursor, cmd, string=None):
    if string:
        print(string)
    for row in cursor.execute(cmd):
        print(row)
    print()


def analyse_ratios(options, cursor):
    try:
        #ratios = cursor.execute("SELECT * FROM ratios;")
        print_top("You message them the most", cursor,
                "SELECT * FROM ratios ORDER BY words_sent DESC")

        # More content = you like them. That's obvious.
        print_top("You send them more content than they do", cursor,
                "SELECT name, quantity FROM ratios ORDER BY quantity DESC")

        # You like them too but not as much as they like you.
        print_top("They send you more content than you do", cursor,
                "SELECT name, quantity FROM ratios ORDER BY quantity")

        # Longer messages => ?? Half is "i don't really know you" and the other
        # half is "I know you too much so I'm okay spamming you"
        print_top("Your message are longer with them", cursor,
                "SELECT name, u_quality FROM ratios ORDER BY u_quality DESC")

        print_top("They message you the longer", cursor,
                "SELECT name, p_quality FROM ratios ORDER BY p_quality DESC")

        # Shorter messages ==> feeling okay/friendly?
        print_top("Your messages are shorter with them", cursor,
                "SELECT name, u_quality FROM ratios ORDER BY u_quality")

        print_top("They message you the shorter", cursor,
                "SELECT name, p_quality FROM ratios ORDER BY p_quality")

        # Guys in the intersection (both shorter messages) <=> your preferred
        # interlocutor?
        print_result(cursor,
                "SELECT name FROM ratios ORDER BY u_quality LIMIT 10 \
                INTERSECT \
                SELECT name FROM ratios ORDER BY p_quality LIMIT 10",
                string="Preferred interlocutors")

    except lite.Error as e:
        update_ratios(options, cursor)
        analyse_ratios(options, cursor)

def analyse(options, cursor):
    try:
        print_result(cursor, "SELECT name, count(sender_id) \
                FROM Messages \
                JOIN Interlocutors ON Interlocutors.id=sender_id \
                GROUP BY sender_id ORDER BY count(sender_id) DESC")
        analyse_ratios(options, cursor)

    except lite.Error as e:
        print("Error: %s" % e.args[0])
        sys.exit(1)


def read_database(options):
    con = None
    try:
        con = lite.connect("user.db")
        cursor = con.cursor()

        #TODO: Use result below to check update
        print_result(cursor, "SELECT name, updated_time, reached_end \
                FROM Retrieving_stats \
                JOIN Interlocutors ON Interlocutors.id=contact_id")

        if options.update:
            update_ratios(options, cursor)

        analyse(options, cursor)

    except lite.Error as e:
        print("Error: %s" % e.args[0])
        sys.exit(1)

    finally:
        if con:
            con.close()

