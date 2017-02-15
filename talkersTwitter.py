#!/usr/bin/env python

#Title      : TwitterScraper
#Author     : Gerry Grant
#Date       : Feb 2017
#File       : twitterScraper.py
#Version    : 0.0.1
#Description: Script to gather info on Twitter users.

#Set imports
import twitter
import datetime
from dateutil import parser
from geopy.geocoders import Nominatim

#Set variables and api tokens and secrets
apiKey = ""
apiSecret = ""
accessToken = ""
accessSecret = ""

#Create Twitter class
t = twitter.Api(consumer_key=apiKey,
                  consumer_secret=apiSecret,
                  access_token_key=accessToken,
                  access_token_secret=accessSecret, sleep_on_rate_limit=True)

#Create location class
geolocate = Nominatim()

def menu():
    #Function to hold menu options
    
    print "1. Search for a name"
    print "2. Analyse User"
    print "99. Quit"
    option = raw_input("Enter selection: ")
    #Put in a fall back incase someone doesn't select a number
    return int(option)

def get_followers(screen_name):

    return t.GetFollowers(screen_name=screen_name)

def get_friends(screen_name):

    return t.GetFriends(screen_name=screen_name)

def search_user_option():
    
    page = 0
    pick = 999
    option = 1
    result = []
    name = raw_input("Enter name to search: ")
    while pick == 999:
        page += 1
        search = search_user(name, page)
 
        for u in search:
            result.append(u)
            print option," ",u.name," @",u.screen_name," ",u.location
            option += 1
        print 999, "More results"
 
        pick = int(raw_input("Select user: "))
        
    return get_user(result[pick-1].screen_name)

def search_user(name, page):
    #Should really put this in a try/catch
    return t.GetUsersSearch(term=name, page=page)

def get_user(name):

    return t.GetUser(screen_name=name)

def analyse_user(user):

    
    print "Basic Info"
    print "Name: ", user.name
    print "Twitter ID: ",user.id
    print "Location: ",user.location
    print "Tweets per day: ",int(user.statuses_count)/date_from_start(user)
    print "Email: ",user.email
    print "Website: ",user.url
    print "Bio: ",user.description
    print "Geo tagging: ",user.geo_enabled
    print "Verified: ",user.verified
    print "Protected: ",user.protected
    print "Timezone: ",user.time_zone
    print "*******************************"
    print "Checking tweets ..............."
    analyse_tweets(user)
    print
    print "*******************************"
    print "Possible interesting followers:"
    mutual = get_mutual(get_followers(user.screen_name),get_friends(user.screen_name))
    for i in mutual:
        print i.screen_name
    print "******END OF REPORT****"


def analyse_tweets(user):

    tweets = t.GetUserTimeline(screen_name=user.screen_name, count=200)
    print len(tweets), " tweets analysed."
    print
    source = {}
    places = {}
    coor = {}
    poss_url = []
    
    for tw in tweets:
        if tw.source[tw.source.find('>')+1:tw.source.find('</')] not in source:
            source[tw.source[tw.source.find('>')+1:tw.source.find('</')]] = [tw.text]
            if len(tw.urls) > 0:
                poss_url.append(tw.urls[0].expanded_url)
                
        else:
            source[tw.source[tw.source.find('>')+1:tw.source.find('</')]] += [tw.text]

        if tw.place is not None:
            if tw.place['full_name'] not in places:
                places[tw.place['full_name']] = [tw.text]

            else: places[tw.place['full_name']].append(tw.text)

        if tw.coordinates is not None:
            location = geolocate.reverse(str(tw.coordinates['coordinates'][1])+','
                                         +str(tw.coordinates['coordinates'][0])).address
            if location not in coor:
                coor[location] = [tw.text]
            else: coor[location].append([tw.text])

    print "Sources of tweets:"
    for key in source:
        print key, " used ",len(source[key])," times"
    print
    print "Possible locations:"
    for key in places:
        print key,":"
        for i in places[key]:
            print i
        print

    print
    print "Geo tagged tweets:"
    for key in coor:
        print key,":"
        for i in coor[key]:
            print i
    print
    print "Possible other links: "
    for i in poss_url:
        print i

def date_from_start(user):

    today = datetime.date.today()
    start = parser.parse(user.created_at)
    start = start.date()
    days = today-start
    
    return days.days

def get_mutual(follow, friends):

    mutual = []

    for i in friends:
        if i in follow:
            mutual.append(i)

    return mutual


while True:
    option = menu()

    if option == 1:
        user = search_user_option()
        analyse_user(user)

    elif option == 2:
        user = raw_input("Enter user screen name: ")
        analyse_user(get_user(user))

    elif option == 99:
        break

        
        

        
