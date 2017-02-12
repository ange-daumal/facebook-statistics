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

def print_top(options, string, cursor, cmd):
    print(string)
    for result in cursor.execute(cmd + " LIMIT %d;" % options.limit):
        print(result)
    print()

def analyse_ratios(options, cursor):
    try:
        #ratios = cursor.execute("SELECT * FROM ratios;")
        print_top(options, "You message them the most", cursor,
                "SELECT * FROM ratios ORDER BY words_sent DESC")

        # More content = you like them. That's obvious.
        print_top(options, "You send them more content than they do", cursor,
                "SELECT name, quantity FROM ratios ORDER BY quantity DESC")

        # You like them too but not as much as they like you.
        print_top(options, "They send you more content than you do", cursor,
                "SELECT name, quantity FROM ratios ORDER BY quantity")

        # Longer messages => ?? Half is "i don't really know you" and the other
        # half is "I know you too much so I'm okay spamming you"
        print_top(options, "Your message are longer with them", cursor,
                "SELECT name, u_quality FROM ratios ORDER BY u_quality DESC")

        print_top(options, "They message you the longer", cursor,
                "SELECT name, p_quality FROM ratios ORDER BY p_quality DESC")

        # Shorter messages ==> feeling okay/friendly?
        print_top(options, "Your messages are shorter with them", cursor,
                "SELECT name, u_quality FROM ratios ORDER BY u_quality")

        print_top(options, "They message you the shorter", cursor,
                "SELECT name, p_quality FROM ratios ORDER BY p_quality")

        # Guys in the intersection (both shorter messages) <=> your preferred
        # interlocutor?

    except lite.Error as e:
        update_ratios(options, cursor)
        analyse_ratios(options, cursor)

