import sqlite3 as lite
import sys
import time
from datetime import date, datetime, timedelta
from utils import url_to_json

def try_execute(cursor, str):
    try:
        cursor.execute(str)
    except lite.Error as e:
        print("Error: %s" % e.args[0])
        raise

def create_tables(cursor):
    try_execute(cursor, "CREATE TABLE IF NOT EXISTS Interlocutors( \
            id VARCHAR(64) UNIQUE NOT NULL, \
            name VARCHAR(64) NOT NULL, \
            sex CHAR(1), \
            PRIMARY KEY(id) \
            );")
    try_execute(cursor, "CREATE TABLE IF NOT EXISTS Messages( \
            id VARCHAR(64) UNIQUE NOT NULL, \
            sender_id VARCHAR(64) NOT NULL, \
            recipient_id VARCHAR(64) NOT NULL, \
            time DATETIME NOT NULL, \
            content VARCHAR(20000) NOT NULL, \
            PRIMARY KEY (id), \
            FOREIGN KEY (sender_id) REFERENCES Interlocutors(id), \
            FOREIGN KEY (recipient_id) REFERENCES Interlocutors(id) \
            );")
    try_execute(cursor, "CREATE TABLE IF NOT EXISTS Retrieving_stats( \
            contact_id VARCHAR(64) UNIQUE NOT NULL, \
            updated_time DATETIME NOT NULL, \
            reached_end BIT NOT NULL, \
            FOREIGN KEY (contact_id) REFERENCES Interlocutors(id));")

def try_execute_easy(cursor, str):
    try:
        cursor.execute(str)
    except lite.IntegrityError:
        pass
    except lite.Error as e:
        print("Error: %s" % e.args[0])
        raise

def reset_tables(cursor):
   try_execute(cursor, "DROP TABLE IF EXISTS Messages;")
   try_execute(cursor, "DROP TABLE IF EXISTS Interlocutors;")

def add_interlocutors(cursor, user, partner):
    try_execute_easy(cursor,
            "INSERT INTO Interlocutors VALUES ('{}', '{}', {});".format(
                user.id, user.username, 1 if user.gender=="female" else 0))

    try_execute_easy(cursor,
            "INSERT INTO Interlocutors VALUES ('{}', '{}', {});".format(
                partner.id, partner.username, "NULL"))

    try_execute_easy(cursor,
            "INSERT INTO Retrieving_stats VALUES ('{}', '{}', {});".format(
        partner.id, datetime.now(), 0))

def date_conversion(s):
    return s.replace("T", " ").split("+")[0]


def insert_message(cursor, msg_id, sender, receiver, datetime, msg):
    # I am not using try_execute_easy because of syntax errors due to
    # the string 'msg' not escaped. Escaping with re.sub() or re.escape()
    # do not seem enough to cover it, so...
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
            print("%s| %s" % (message['from']['name'], message['message']))
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


def reached_end(options, cursor, partner, now):
    try:
        cursor.execute("UPDATE Retrieving_stats SET reached_end=1, \
                updated_time=? WHERE contact_id=?;",
                [now, partner.id])
        if options.debug:
            print("Synch finished! Last updated: %s " % now)
    except lite.Error as e:
        print("Error: %s" % e.args[0])
        raise


def loop_messages(options, con, message_page, user, partner):
    cur = con.cursor()
    # Get messages-retrieving tracking stats
    stats = cur.execute("SELECT updated_time, reached_end \
            FROM Retrieving_stats \
            JOIN Interlocutors ON Interlocutors.id=contact_id\
            WHERE contact_id='{}'".format(partner.id)).fetchone()
    now = datetime.now()

    for i in range(options.n):
        messages = message_page['data']
        for message in messages:
            add_message(options, cur, user, partner, message)
        con.commit()

        if (not 'paging' in message_page.keys() or
        stats[1] == 1 and message['created_time'] > stats[0]):
            return reached_end(options, cur, partner, now)
        else:
            time.sleep(options.s)
            message_page = url_to_json(message_page['paging']['next'])


def save_messages(options, con, inbox, user, partner, interlocutor_limit=2):
    # Looking for interlocutor
    for i in range(options.l):
        for conversation_list in inbox['data']:
            to = conversation_list['to']['data']
            if len(to) <= interlocutor_limit and len(to) > 1:
                interlocutor = to[0] if to[1]['id'] == user.id else to[1]
                # Found
                if interlocutor['id'] == partner.id:
                    return loop_messages(options, con,
                            conversation_list['comments'], user, partner)
        inbox = url_to_json(inbox['paging']['next'])


def fill_database(options, user, partner, inbox):
    con = None
    try:
        con = lite.connect("user.db")
        cursor = con.cursor()

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

