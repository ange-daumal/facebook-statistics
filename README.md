# facebook-statistics

This project is an open source tool built to analyse your Facebook data
and provide you some satisfying graphs.

Please feel free to suggest us whatever you'd like to see added to
our TODO list ;)

# Installation

## Requirements

* Python3.5
* pip
* packages listed in requirements.txt : run `pip install -r requirements.txt`

## Setup for Facebook API

* Go to https://developers.facebook.com/tools/explorer/
* Click on "Get Token". "Select Permissions" window appears. "In the top-right,
change the latest version to 2.3
* In "Other", check "read_mailbox"
* Click on Get Access Token
* Copy paste the access token in a new file named "user.settings".

Warning : this access token will only last few hours, so do not forget to
update it before every use of the program.

## Setup for MySQL Database

* Install mysql https://dev.mysql.com/doc/refman/5.5/en/installing.html
* Choose a username, a password and a database name. For example, we choose
username="scott", password="pwd" and database's name is "messages". Don't
forget to replace these examples by yours in the following steps.
* Launch my sql `su; mysql`
* Create your user `CREATE USER "scott"@"localhost" IDENTIFIED BY "pwd";`
* And create the database `CREATE DATABASE messages;`
* Now enter your datas in a file named "mysql.settings" like this :
```
username=scott
password=pwd
database=messages
```

You're all set!

# Troubleshoot

If you deleted messages that you have sent or received, we won't be
able to retrieve them.

## New to Python

### On Linux

Follow these commands:
```
sudo apt-get install python3 python3-pip
pip install -m --upgrade pip
```
Commands `python` and `pip` should work directly from your terminal.
If not, you can add their path to your environment variables or use an alias.

### On Windows

* Install the last release of python *3* from www.python.org

Then I'll recommand download a Python IDE, like PyCharm. It will automatically
download all the needed packages when you open the project.
