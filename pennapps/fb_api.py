# -*- coding: utf-8 -*-
from pyfb import Pyfb
from settings import FACEBOOK_APP_ID, FACEBOOK_SECRET_KEY, RDIO_KEY, RDIO_SECRET, LAST_API_KEY, LAST_SECRET, LAST_USERNAME, LAST_PASSWORD
import sys
from collections import Counter
import json
from rdio import Rdio
import pylast
import time
import re


#token = 'CAAUz0srmPAUBAAixz93XR3rVXF0ATBCs9ZC3vKb5I9HTOYknJYTmRAcBVd3Xm36lWkRkJZCkgVXYbypvZCZCOfzoXJV81mrfZBg2aGqqYwMrPUr0WQSVk4sN6zyP0xZCrvvoZBeJsWZCSOoEICAUVOdgHMROgvr3Rjsr0ngZBtASdVr1mQFh1VgwPvTjcAFXZCrsPzZCdzeUH7DegZDZD'
fb = Pyfb(FACEBOOK_APP_ID)
rdio = Rdio((RDIO_KEY, RDIO_SECRET))
NUMBER_OF_PEOPLE = 100

API_KEY = LAST_API_KEY 
API_SECRET = LAST_SECRET

username = LAST_USERNAME
password_hash = pylast.md5(LAST_PASSWORD)

network = pylast.LastFMNetwork(api_key = API_KEY, api_secret = 
    API_SECRET, username = username, password_hash = password_hash)
	
def find_artist_id(artist_name):
	# results are returned in multiple layers of dictionaries and lists
	# the following lines extract the useful information
	artist_list = (rdio.call('search',params={'query': artist_name, 'types': 'Artist'})['result'])\
	['results']
	if artist_list == []:
		# checks if there are any artists with the given name in the database
		return ""
	else:
		# return the first available artist with the given name. This assumes that 
		# the most famous artist will appear first
		return artist_list[0]['key'].encode('utf-8', errors='replace')
		
		
def find_artist_image(artist_id):
	return rdio.call('getTracksForArtist',params={'artist': artist_id,'sort':'playCount','count':5})\
	['result'][0]['icon'].encode('utf-8', errors='replace')
	
def find_songs(artist_id):
	if artist_id=="":
		return []
	x = rdio.call('getTracksForArtist',params={'artist': artist_id,'sort':'playCount','count':5})\
	['result']
	if x == []:
		return []
	songlist = []
	for i in reversed(xrange(5)):
		try:
			l = x[i]['name'][:46]
			if len(l) == 46:
				l = l[:43]+"..."
			songlist.append(l.replace("'","").encode('utf-8', errors='replace'))
		except: return []
	return songlist
	
def get_genre(artist):
	artist = network.get_artist(artist)
	topItems = artist.get_top_tags(limit=5)
	genre_string = []
	for topItem in topItems:
		genre_string.append(topItem.item.get_name().title().replace("'","").encode('utf-8', errors='replace'))
	for genre in genre_string:
		if genre in ['House', 'Electronic', 'EDM', 'Dubstep', 'DnB']:
			return 'Electronic'
		elif genre in ['Rock', 'Metal', 'Heavy Metal' 'Thrash Metal', 'Death Metal']:
			return 'Rock/Metal'
		elif genre in ['Alternative', 'Indie']:
			return 'Alternative'
		elif genre in ['Country', 'Folk']:
			return 'Country/Folk'
		elif genre in ['Classic Rock', 'Pop', 'Classical', 'Jazz', 'Hip-Hop', 'Reggae', 'Rap']:
			return genre
	return 'Other'

def get_facebook_friends(user_id, token):
	friend_list = []
	friends = fb.get_friends(user_id)
	friends = friends[:NUMBER_OF_PEOPLE]
	friend_list = [friend.id.encode('utf-8', errors='replace') for friend in friends]
	return friend_list

def get_event_id_from_url(url):
	pattern=re.search(r'/events/(\d+)/', url)
	return pattern.group(1)
	
def get_event_members(event_id):
	members = fb.fql_query("SELECT uid FROM event_member WHERE eid = %r AND rsvp_status='attending'" % event_id)
	member_list = []
	member_list = [member.uid for member in members]
	return member_list

def get_music_likes(people_list):
	music_list = []
	for person in people_list:
		music = fb.fql_query("SELECT music FROM user WHERE uid = '%r'" % person)[0].music.encode('utf-8', errors='replace')
		if music is not "":
			(music_list.extend(music.split(",")))
	return Counter(music_list)	
	
def get_artists(counter_list):
	i=0
	dictionary_list=[]
	dictionary={}
	for artist in counter_list:
		if counter_list[artist] > (3): #number here determines min number of likes for artist
			i += 1
			artist_id=find_artist_id(artist)
			songs=find_songs(artist_id)
			if songs == [] or artist_id == "":
				continue
			else:
				dictionary["songs"] = songs
				dictionary["id"] = artist_id
			dictionary["likes"] = counter_list[artist]
			dictionary["name"] = artist.replace("'","")
			try:
				dictionary["imageUrl"] = find_artist_image(artist_id)
			except:
				dictionary["imageUrl"] = ""
			try:
				dictionary["genre"] = get_genre(artist)
			except:
				dictionary["genre"] = ""
			dictionary_list.append(dictionary.copy())
	return dictionary_list
	
def format_text(list):
	s = ('[\n')
	countcount = 0 #countcount makes sure there's no , after the last artist
	for item in list:
		s += ('\t{\n')
		counter=0 # if counter==3 or 6, different formatting is required
		a=len(list)
		for key in item:
			if counter == 3:
				s += ("\t\t%r: [" % (key.encode('utf-8', errors='replace')))
				counter2 = 0 #when counter2 reaches 5th attribute, different formatting is required
				for song in item["songs"]:
					s += ("\t\t{\"name\":%r}" % song)
					counter2 += 1
					if counter2 == 5:
						s += ("\n\t\t\t],\n")
						break
					s += (",\n")
				counter += 1
			else:
				s += ("\t\t%r: %r" % (key.encode('utf-8', errors='replace'), item[key]))
				counter += 1
				if counter == 6:
					s += ("\n")
					break
				s += (",\n")
		countcount += 1
		if countcount < a:
			s += ('\t},\n')
		else:
			s += ('\t}\n')
	s += (']')
	s = s.replace("'","\"")
	return s
	
#def json_list(list):
#	return json.dumps(list, sort_keys = True, indent = 4)
	
def run_all(url, token):
	fb.set_access_token(token)
	return format_text(get_artists(get_music_likes(get_event_members(get_event_id_from_url(url)))))

print run_all('https://www.facebook.com/events/250613785109402/')	
