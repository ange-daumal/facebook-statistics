import sqlite3 as lite
import sys
from messages_ratio import compare_words, analyse_ratios

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

def print_result(cursor, cmd, string=None):
    if string:
        print(string)
    for row in cursor.execute(cmd):
        print(row)
    print()

def analyse(options, cursor):
    try:
        if options.debug:
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
        if options.debug:
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

