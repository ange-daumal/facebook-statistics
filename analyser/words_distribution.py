import sqlite3 as lite
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
import numpy as np
import matplotlib.pyplot as plt

from stop_words import get_stop_words

def KL(a, b):
    a = np.asarray(a, dtype=np.float)
    b = np.asarray(b, dtype=np.float)
    return np.sum(np.where(a != 0, a * np.log(a / b), 0))

def cut(options, bunch_of_messages, mult):
    x_trains = []
    msgs = [msg[0] for msg in bunch_of_messages]
    for i in range(int(options.n / mult) + 1):
        truc = msgs[options.n * i:options.n * (i + 1)]
        if options.debug:
            print("%d ([%d:%d => %0.2f]) : %s" % (i, options.n*i,
            options.n * (i+1), len(truc), truc))
        x_trains.append(truc)
    return x_trains



def analyse_words(options, cursor, contact_id):
    mult = 5
    bunch_of_messages = cursor.execute("SELECT content FROM Messages \
            WHERE (sender_id='{0}' OR recipient_id='{0}') \
            ORDER BY time \
            LIMIT {1};".format(contact_id, options.n * mult))

    X_trains = []
    tfidf_vect = TfidfVectorizer(analyzer="word", ngram_range=(1, 3),
            stop_words=get_stop_words("french") + get_stop_words("english"))

    x_trains = cut(options, bunch_of_messages, mult)
    # hard-coded because testing reasons!
    labels = ['metal', 'photoshop', 'autisme', 'check presence', 'dormir']
    true_k = len(labels)

    for x_train in x_trains:
        X_train = tfidf_vect.fit_transform(x_train)
        X_trains.append(X_train)
        print()
        print(X_train.shape)
        #print(tfidf_vect.vocabulary_)

    print()
    if options.debug:
        print("*** Start Clustering!")
    kmeans = KMeans(n_clusters=5).fit(X_trains[0])
    print(kmeans.labels_)
    print(kmeans.cluster_centers_)

