
all: init
	time python retriever/__init__.py -n 500 --all
	time python analyser/__init__.py

all3: init3
	time python3 retriever/__init__.py -n 500 --all
	time python3 analyser/__init__.py

help:
	python3 retriever/__init__.py -h

init:
	pip install -r requirements.txt --upgrade pip

init3:
	sudo -H python3 -m pip install -r requirements.txt --upgrade pip

reset:
	rm user.db user.settings

.PHONY: help init reset
