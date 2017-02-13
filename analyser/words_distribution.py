import sqlite3 as lite
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer
from stop_words import get_stop_words
import numpy as np

def KL(a, b):
    a = np.asarray(a, dtype=np.float)
    b = np.asarray(b, dtype=np.float)
    return np.sum(np.where(a != 0, a * np.log(a / b), 0))

#def clusterise(messages, n=5):


def analyse_words(options, cursor, contact_id):
    bunch_of_messages = cursor.execute("SELECT content FROM Messages \
            WHERE (sender_id='{0}' OR recipient_id='{0}') \
            ORDER BY time \
            LIMIT {1};".format(contact_id, options.n * 5))

    x_trains = []
    msgs = [msg[0] for msg in bunch_of_messages]
    print("clusters: %d |" % len(msgs))
    print(msgs)
    print()
    for i in range(options.n):
        truc = msgs[options.n * i:options.n * (i + 1)+options.n]
        if options.debug:
            print("%d ([%d:%d => %0.2f]) : %s" % (i, options.n*i,
            options.n * (i+1), len(truc), truc))
        x_trains.append(truc)

    print(x_trains)
    print()

    for x_train in x_trains:
        print(x_train)
        count_vect = CountVectorizer(analyzer="word", ngram_range=(1, 3),
                stop_words=get_stop_words("french") + get_stop_words("english"))
        X_train = count_vect.fit_transform(x_train)
        print(X_train.shape)
        print()
        print(count_vect.vocabulary_)
        print()
        '''
        x_train2 = x_trains[1]
        tfidf_vect = TfidfVectorizer(analyzer="word", ngram_range=(1, 3),
                stop_words=get_stop_words("french") + get_stop_words("english"))
        X_train2 = tfidf_vect.fit_transform(x_train2)
        print()
        print(X_train2.shape)
        print(tfidf_vect.vocabulary_)
        print()
        '''
