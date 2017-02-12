
all:
	time python3 retriever/__init__.py -n 500 --all
	time python3 analyser/__init__.py

help:
	python3 retriever/__init__.py -h

init:
	pip install -r requirements.txt

reset:
	rm user.db user.settings
