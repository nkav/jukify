# -*- coding: utf-8 -*-
from pyfb import Pyfb
from settings import FACEBOOK_APP_ID, FACEBOOK_SECRET_KEY, RDIO_KEY, RDIO_SECRET, LAST_API_KEY, LAST_SECRET, LAST_USERNAME, LAST_PASSWORD
import sys
from collections import Counter
import json
from rdio import Rdio
import pylast


fb = Pyfb(FACEBOOK_APP_ID)
rdio = Rdio((RDIO_KEY, RDIO_SECRET))
NUMBER_OF_PEOPLE = 100

API_KEY = LAST_API_KEY 
API_SECRET = LAST_SECRET

username = LAST_USERNAME
password_hash = pylast.md5(LAST_PASSWORD)

network = pylast.LastFMNetwork(api_key = API_KEY, api_secret = 
    API_SECRET, username = username, password_hash = password_hash)
	
#Copy the [access_token] and enter it below

#token = 'CAAUz0srmPAUBAPSn6sapqSuVC13vVICyp7dsyLKZBHRM1ZCjpQlZBx3aqOLI1DFqxMa3KE5wXBLmgtVSsnHpakalpayt3xyNwrnwGuo98XHpeOhDzpZBYLM1dhpw1ORnOilob2xPbb75SXjDGOZBrlU5cdZC6d6ZBF79niutS4JzMA2D6ABvBS8L0DYi6dO2R6f9Q8tX8AQEwZDZD'
#Sets the authentication token


def find_artist_id(artist_name):
	artistname = artist_name.encode('utf-8', errors='replace')
	x=rdio.call('search',params={'query': artist_name, 'types': 'Artist'})
	# results are returned in multiple layers of dictionaries and lists
	# the following lines extract the useful information
	y = x['result']
	z = y['results']
	if z == []:
		return ""
	else:
		q = z[0]
		w = q['key'].encode('utf-8', errors='replace')
		return w

def find_artist_image(artist):
	artistkey = find_artist_id(artist)
	x = rdio.call('getTracksForArtist',params={'artist': artistkey,'sort':'playCount','count':5})
	y = x['result']
	z = y[0]
	c = z['icon'].encode('utf-8', errors='replace')
	return c
	
def find_songs(artist):
	artistkey = find_artist_id(artist)
	if artistkey=="":
		return []
	x = rdio.call('getTracksForArtist',params={'artist': artistkey,'sort':'playCount','count':5})
	y = x['result']
	if y == []:
		return []
	songlist = []
	for i in range(0,5):
		z = y[i]
		k = z['name']
		l = k[:46]
		if len(l) == 46:
			l = l[:43]+"..."
		songlist.append(l.replace("'","").encode('utf-8', errors='replace'))
	return songlist
	
def get_genre(artist):
	artist = network.get_artist(artist)
	topItems = artist.get_top_tags(limit=None)
	for topItem in topItems:
		a = topItem.item.get_name().title().replace("'","").encode('utf-8', errors='replace')
		if a in ['House', 'Electronic', 'EDM', 'Dubstep', 'DnB']:
			return 'Electronic'
		elif a in ['Rock', 'Metal', 'Heavy Metal' 'Thrash Metal', 'Death Metal']:
			return 'Rock/Metal'
		elif a in ['Alternative', 'Indie']:
			return 'Alternative'
		elif a in ['Country', 'Folk']:
			return 'Country/Folk'
		elif a in ['Classic Rock', 'Pop', 'Classical', 'Jazz', 'Hip-Hop', 'Reggae', 'Rap']:
			return a
		else:
			return 'Other'

def get_artists(user_id, token):
	fb.set_access_token(token)
	list = []
	dictionarylist = []
	dictionary = {}
	i = 0
	friends = fb.get_friends(user_id)
	for friend in friends:
		if i < NUMBER_OF_PEOPLE:
			a = fb.get_likes(friend.id)
			while (a):
				for like in a:
					if like.category == "Musician/band":
						list.append(like.name.encode('utf-8', errors='replace'))
				a = a.next()
			i = i + 1
			print friend.name.encode('utf-8', errors='replace') +" %d" % i
	for item in list:
		sys.stderr.write("List" + item + '\n')
	b = Counter(list)
	i=0
	for artist in b:
		sys.stderr.write("Counter" + artist + '\n')
		sys.stderr.write(str(b[artist]) + '\n')
		if b[artist] > (NUMBER_OF_PEOPLE/20):
			sys.stderr.write("Counter" + artist + '\n')
			i=i+1
			if find_songs(artist) == [] or find_artist_id(artist) == "":
				continue
			dictionary["likes"] = b[artist]
			dictionary["name"] = artist.replace("'","")
			try:
				dictionary["id"] = find_artist_id(artist)
			except:
				dictionary["id"] = ""
			try:
				dictionary["songs"] = find_songs(artist)
			except:
				dictionary["songs"] = ""
			try:
				dictionary["imageUrl"] = find_artist_image(artist)
			except:
				dictionary["imageUrl"] = ""
			try:
				dictionary["genre"] = get_genre(artist)
			except:
				dictionary["genre"] = ""
			dictionarylist.append(dictionary.copy())
	return dictionarylist
	
def format_text(list):
	s=""
	s+=('[\n')
	countcount=0
	for item in list:
		s+=('\t{\n')
		counter=0
		a=len(list)
		for key in item:
			if counter ==3:
				s+=("\t\t%r: [" % (key.encode('utf-8', errors='replace')))
				counter2=0
				for song in item["songs"]:
					s+=("\t\t{\"name\":%r}" % song)
					counter2=counter2+1
					if counter2==5:
						s+=("\n\t\t\t],\n")
						break
					s+=(",\n")
				counter=counter+1
			else:
				s+=("\t\t%r: %r" % (key.encode('utf-8', errors='replace'), item[key]))
				counter=counter+1
				if counter == 6:
					s+=("\n")
					break
				s+=(",\n")
		countcount=countcount+1
		if countcount<a:
			s+=('\t},\n')
		else:
			s+=('\t}\n')
	s+=(']')
	s=s.replace("'","\"")
	return s
	
	
def json_list(list):
	return json.dumps(list, sort_keys = True, indent = 4)

#f=open("sample.txt","w")
#f.write(json_list(get_artists('sebastian.rollen', token)))
