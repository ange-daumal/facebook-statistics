import sqlite3 as lite

def analyse_words(options, cursor, contact_id):
    bunch_of_messages = cursor.execute("SELECT content FROM Messages \
            WHERE (sender_id='{0}' OR recipient_id='{0}') \
            ORDER BY time \
            LIMIT {1};".format(contact_id, options.n))
    for msg in bunch_of_messages:
        print(msg)
