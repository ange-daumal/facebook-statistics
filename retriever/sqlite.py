import sqlite3 as lite
import sys
from datetime import date, datetime, timedelta
from utils import url_to_json

def create_tables(cursor):
    try:
        cursor.execute("CREATE TABLE IF NOT EXISTS Interlocutors( \
                id VARCHAR(64) UNIQUE NOT NULL, \
                name VARCHAR(64) NOT NULL, \
                sex CHAR(1), \
                PRIMARY KEY(id) \
                );")
    except lite.Error as e:
        print("Error: %s" % e.args[0])
        raise
        sys.exit(1)
    try:
        cursor.execute("CREATE TABLE IF NOT EXISTS Messages( \
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
        raise
        sys.exit(1)
    try:
        cursor.execute("CREATE TABLE IF NOT EXISTS Retrieving_stats( \
                contact_id VARCHAR(64) UNIQUE NOT NULL, \
                updated_time DATETIME NOT NULL, \
                reached_end BIT NOT NULL, \
                FOREIGN KEY (contact_id) REFERENCES Interlocutors(id));")
    except lite.Error as e:
        print("Error: %s" % e.args[0])
        raise
        sys.exit(1)
    return

def reset_tables(cursor):
    try:
        cursor.execute("DROP TABLE IF EXISTS Messages;")
        cursor.execute("DROP TABLE IF EXISTS Interlocutors;")
    except lite.Error as e:
        print("Error: %s" % e.args[0])

def try_command(cursor, command):
    try:
        cursor.execute(command)
    except lite.IntegrityError:
        pass
    except lite.Error as e:
        print("Error: %s" % e.args[0])
        raise
        sys.exit(1)

def add_interlocutors(cursor, user, partner):
    try_command(cursor, "INSERT INTO Interlocutors VALUES ('{}', '{}', {});".format(
                user.id, user.username, 1 if user.gender=="female" else 0))

    try_command(cursor, "INSERT INTO Interlocutors VALUES ('{}', '{}', {});".format(
                partner.id, partner.username, "NULL"))

    try_command(cursor, "INSERT INTO Retrieving_stats VALUES ('{}', '{}', {});".format(
        partner.id, datetime.now(), 0))

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
    return

def reached_end(options, cursor, partner):
    if options.debug:
        print("REACHED END!!")
    try:
        cursor.execute("UPDATE Retrieving_stats SET reached_end=1, \
                updated_time=? WHERE contact_id=?;",
                [datetime.now(), partner.id])
    except lite.Error as e:
        print("Error: %s" % e.args[0])
        raise
    return

def loop_messages(options, con, message_page, user, partner):
    cur = con.cursor()
    stats = cur.execute("SELECT updated_time, reached_end \
            FROM Retrieving_stats \
            JOIN Interlocutors ON Interlocutors.id=contact_id\
            WHERE contact_id='{}'".format(partner.id)).fetchone()

    for i in range(options.n):
        messages = message_page['data']
        for message in messages:
            add_message(options, cur, user, partner, message)
        con.commit()

        if stats[1] == 1 and message['created_time'] > stats[0]:
            if options.debug:
                print("Synch finished! Last updated: %s " % (stats[0]))
            return

        if 'paging' in message_page.keys():
            message_page = url_to_json(message_page['paging']['next'])
        else:
            return reached_end(options, cur, partner)


def save_messages(options, con, inbox, user, partner, interlocutor_limit=2):
    # Looking for interlocutor
    for i in range(options.l):
        for conversation_list in inbox['data']:
            to = conversation_list['to']['data']
            if len(to) <= interlocutor_limit and len(to) > 1:
                interlocutor = to[0] if to[1]['id'] == user.id else to[1]
                if interlocutor['id'] == partner.id:
                    return loop_messages(options, con,
                            conversation_list['comments'], user, partner)
        inbox = url_to_json(inbox['paging']['next'])


def fill_database(options, user, partner, inbox):
    con = None
    try:
        con = lite.connect("user.db")
        cursor = con.cursor()
    except lite.Error as e:
        print("Error: %s" % e.args[0])
        raise

    try:
        if options.reset:
            reset_tables(cursor)

        create_tables(cursor)
        add_interlocutors(cursor, user, partner)
        save_messages(options, con, inbox, user, partner)

    except lite.Error as e:
        print("Error: %s" % e.args[0])
        raise
    finally:
        con.commit()
        con.close()
    return

