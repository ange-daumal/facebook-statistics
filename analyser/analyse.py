import sqlite3 as lite
import sys

def get_interlocutor_id(options, cursor, name):
    return cursor.execute("SELECT id FROM Interlocutors WHERE name=%s" % name)

def count_words(options, cursor):
    for row in cursor.execute("SELECT content FROM Messages WHERE"):
        print(row)

def read_database(options):
    con = None
    try:
        con = lite.connect("user.db")
        cursor = con.cursor()

        if options.contact:
            print(options.contact)
            contact_id = get_interlocutor_id(options, cursor, options.contact)
            print(contact_id)

        else:
            for row in cursor.execute("SELECT name, count(sender_id) FROM Messages JOIN Interlocutors ON Interlocutors.id=sender_id GROUP BY sender_id"):
                print(row)

    except lite.Error as e:
        print("Error: %s" % e.args[0])
        sys.exit(1)

    finally:
        if con:
            con.close()

