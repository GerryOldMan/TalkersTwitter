# TalkersTwitter
Python script to search for Twitter users and extract key information such as webiste, location based tweets, possible links to other social media sites and other persons that might be of interest.

This script uses the python-twitter library (found at https://github.com/bear/python-twitter) and also geopy module (https://github.com/geopy/geopy)

These need to be installed prior to running. 

In order to use the python-twitter API client, you first need to acquire a set of application tokens. These will be your consumer_key and consumer_secret, which get passed to twitter.Api() when starting your application. Follow the instructions here https://python-twitter.readthedocs.io/en/latest/getting_started.html

Run talkersTwitter.py

This offers a menu to either search a name or analyse a user.

To search a name, just enter the name of person and a list of possible users is returned. Select on user to analse that account.

To analyse a user, you need to know their twitter handle. Enter this (without the @) and this should analyse the user.

