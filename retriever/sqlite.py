import mysql.connector
import MySQLdb
import sqlite3 as lite
import sys
from datetime import date, datetime, timedelta
from utils import url_to_json

def create_tables(cursor):
    try:
        cursor.execute("CREATE TABLE Interlocutors( \
                id VARCHAR(64) UNIQUE NOT NULL, \
                name VARCHAR(64) NOT NULL, \
                sex CHAR(1), \
                PRIMARY KEY(id) \
                );")
    except lite.Error as e:
        print("Error: %s" % e.args[0])
    try:
        cursor.execute("CREATE TABLE Messages( \
                id VARCHAR(64) UNIQUE NOT NULL, \
                sender_id VARCHAR(64) NOT NULL, \
                recipient_id VARCHAR(64) NOT NULL, \
                time DATETIME NOT NULL, \
                content VARCHAR(20000) NOT NULL, \
                PRIMARY KEY (id), \
                FOREIGN KEY (sender_id) REFERENCES Interlocutors(id), \
                FOREIGN KEY (recipient_id) REFERENCES Interlocutors(id) \
                );")
    except lite.Error as e:
        print("Error: %s" % e.args[0])
    return

def reset_tables(cursor):
    try:
        cursor.execute("DROP TABLE IF EXISTS Messages;")
        cursor.execute("DROP TABLE IF EXISTS Interlocutors;")
    except lite.Error as e:
        print("Error: %s" % e.args[0])


def add_interlocutors(cursor, user, partner):
    try:
        cursor.execute("INSERT INTO Interlocutors VALUES (?, ?, ?)",
                [user.id, user.username, user.gender])
    except lite.IntegrityError:
        pass
    except lite.Error as e:
        print("Error: %s" % e.args[0])
    try:
        cursor.execute("INSERT INTO Interlocutors VALUES (?, ?, ?)",
                [partner.id, partner.username, "NULL"])
    except lite.IntegrityError:
        pass
    except lite.Error as e:
        print("Error: %s" % e.args[0])
    return


def see_database(options):
    con = None
    try:
        con = lite.connect("user.db")
        cursor = con.cursor()
        for row in cursor.execute("SELECT sender_id, count(id) FROM Messages GROUP BY sender_id"):
            print(row)
        for row in cursor.execute("SELECT * FROM Interlocutors"):
            print(row)
    except lite.Error as e:
        print("Error: %s" % e.args[0])
        sys.exit(1)

    finally:
        if con:
            con.close()


def date_conversion(s):
    return s.replace("T", " ").split("+")[0]

def insert_message(cursor, msg_id, sender, receiver, datetime, msg):
    try:
        cursor.execute("INSERT INTO Messages VALUES (?, ?, ?, ?, ?);",
            [msg_id, sender, receiver, datetime, msg])
    except lite.IntegrityError:
        pass
    except lite.Error as e:
        print(e)
        print("Error: %s" % e.args[0])

def add_message(options, cursor, user, partner, message):
    try:
        if options.debug:
            print("From: %s Content: %s" %
                    (message['from']['name'], message['message']))
        insert_message(cursor, message['id'], message['from']['id'],
                partner.id if message['from']['id'] == user.id else user.id,
                date_conversion(message['created_time']),
                message['message'] if message['message'] is not None else "")
    except KeyError:
        if options.debug:
            print("***") # may be sticker or images sent
        insert_message(cursor, message['id'], message['from']['id'],
                partner.id if message['from']['id'] == user.id else user.id,
                date_conversion(message['created_time']), "")


def save_messages(options, con, inbox, user, partner, interlocutor_limit=2):
    cur = con.cursor()
    # Looking for interlocutor
    for i in range(options.l):
        for conversation_list in inbox['data']:
            to = conversation_list['to']['data']
            if len(to) <= interlocutor_limit and len(to) > 1:
                interlocutor = to[0] if to[1]['id'] == user.id else to[1]
                if interlocutor['id'] == partner.id:
                    # Found, loop on messages
                    message_page = conversation_list['comments']
                    for i in range(options.n):
                        messages = message_page['data']
                        for message in messages:
                            add_message(options, cur, user, partner, message)
                        message_page = url_to_json(message_page['paging']['next'])
                        con.commit()
        inbox = url_to_json(inbox['paging']['next'])


def fill_database(options, user, partner, inbox):
    con = None
    try:
        con = lite.connect("user.db")
        cursor = con.cursor()
    except lite.Error as e:
        print("Error: %s" % e.args[0])
        sys.exit(1)

    try:
        if options.reset:
            reset_tables(cursor)

        create_tables(cursor)
        add_interlocutors(cursor, user, partner)

        save_messages(options, con, inbox, user, partner)

    except lite.Error as e:
        print("Error: %s" % e.args[0])
    finally:
        con.commit()
        con.close()
    return

