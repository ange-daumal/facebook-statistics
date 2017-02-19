# TODO List

Data retrieving:
[X] One-to-one conversations retriever
[X] Retrieving tracker: did we get to the end of conversation with update time
[X] Optimization by number of messages to retrieve
[ ] Group conversation retrieving

Raw data analysis:
[X] Interlocutor's messages length comparaison
[X] Message's size graph
[ ] Most used words per interlocutor
[ ] Emoticon usage
[ ] Who is reviving conversation
[/] Average answering time

ML Analysis:
[/] Subjects
[ ] Most talked subjects (per interlocutor/discussions)
[ ] Finder of sexual orientation / who you'd like to date (?)

# Priorities

## Messages retrieving

Problems:
* Using a old facebook API (2.3) that will be invailable on July 2017.
Unfortunately it is the last one allowing to read the inbox.
* Calls have a rate limit (per 300 seconds and per day I think ?)
* Token access only last one hour

Solutions:
[/] Reduce the API calls to the essential minimum
[ ] Script an automatic way to get the API token?
[ ] Stop using the API : use a python/PHP script scrolling messenger.com?

## Analyses

[will update this part later]
