import sqlite3 as lite
import sys
from messages_ratio import compare_words, analyse_ratios
from words_distribution import analyse_words

def get_interlocutors_id(options, cursor):
    if options.contact:
        return cursor.execute("SELECT id, name FROM Interlocutors \
                WHERE name='%s'" % options.contact)
    contacts = []
    tuples = cursor.execute("SELECT id, name FROM Interlocutors")
    for contact in tuples:
        contacts.append(contact)
    # This is weird but I don't know why my "tuples" object just do not last.
    print(contacts)
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
            print_result(cursor, "SELECT name, count(sender_id), \
                updated_time, reached_end \
                FROM Messages \
                JOIN Interlocutors ON Interlocutors.id=sender_id \
                JOIN Retrieving_stats ON Interlocutors.id=contact_id \
                GROUP BY sender_id \
                ORDER BY reached_end DESC, count(sender_id) DESC")

        if options.what in ['all', 'ratios']:
            analyse_ratios(options, cursor)
        if options.what in ['all', 'subjects']:
            if not options.contact:
                print("Please specify a contact [-c option]")
                sys.exit(1)
            contacts = get_interlocutors_id(options, cursor)
            for contact in contacts:
                analyse_words(options, cursor, contact[0])

    except lite.Error as e:
        print("Error: %s" % e.args[0])
        raise


def read_database(options):
    con = None
    try:
        con = lite.connect("user.db")
        cursor = con.cursor()

        if options.update:
            update_ratios(options, cursor)

        analyse(options, cursor)

    except lite.Error as e:
        print("Error: %s" % e.args[0])
        raise

    finally:
        if con:
            con.close()

