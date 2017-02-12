import sqlite3 as lite
import sys
import datetime

def create_tables(cursor):
    try:
        cursor.execute("CREATE TABLE IF NOT EXISTS Ratio ( \
                contact_id VARCHAR(64) UNIQUE NOT NULL, \
                updated_time DATETIME, \
                words_received INTEGER, \
                messages_received INTEGER, \
                words_sent INTEGER, \
                messages_sent INTEGER, \
                FOREIGN KEY (contact_id) REFERENCES Interlocutors(id) \
                );")
    except lite.Error as e:
        print("Error: %s" % e.args[0])
        sys.exit(1)
    return

def create_view(cursor):
    cursor.execute("DROP VIEW IF EXISTS ratios;")
    cursor.execute("CREATE VIEW ratios AS \
            SELECT name, \
            words_received, messages_received, words_sent, messages_sent, \
            ROUND(CAST(words_sent AS FLOAT) / CAST(words_received AS FLOAT), 2) \
            AS quantity,\
            ROUND(CAST(words_sent AS FLOAT) / CAST(messages_sent AS FLOAT), 2) \
            AS u_quality,\
            ROUND(CAST(words_received AS FLOAT) / CAST(messages_received AS FLOAT), 2) \
            AS p_quality \
            FROM Ratio \
            JOIN Interlocutors ON Interlocutors.id=contact_id;")
    return

def count_words(cursor, contact_id, contact_type):
    contact_messages = 0
    contact_words = 0
    for tuples in cursor.execute("SELECT content FROM Messages \
            WHERE %s=%s" % (contact_type, contact_id)):
        for messages in tuples:
            contact_words += len(messages.split())
        contact_messages += 1
    return contact_words, contact_messages

def compare_words(options, cursor, contacts):
    create_tables(cursor)
    for contact in contacts:
        p_words, p_messages = count_words(cursor, contact[0], "sender_id")
        u_words, u_messages = count_words(cursor, contact[0], "recipient_id")
        try:
            cursor.execute("INSERT INTO Ratio VALUES (?, ?, ?, ?, ?, ?)",
                    [contact[0], datetime.datetime.now(), p_words, p_messages,
                        u_words, u_messages])
        except lite.IntegrityError:
            cursor.execute("UPDATE Ratio SET updated_time=?, words_received=?, \
                    messages_received=?, words_sent=?, messages_sent=? \
                    WHERE contact_id=?",
                    [datetime.datetime.now(), p_words, p_messages,
                        u_words, u_messages, contact[0]])
        except lite.Error as e:
            print("Error: %s" % e.args[0])
            sys.exit(1)
    create_view(cursor)
    return
