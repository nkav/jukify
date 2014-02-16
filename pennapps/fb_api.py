
from pyfb import Pyfb
from settings import FACEBOOK_APP_ID, FACEBOOK_SECRET_KEY, RDIO_KEY, RDIO_SECRET, LAST_API_KEY, LAST_SECRET, LAST_USERNAME, LAST_PASSWORD
import sys
from collections import Counter
import json
from rdio import Rdio
import pylast


fb = Pyfb(FACEBOOK_APP_ID)
rdio = Rdio((RDIO_KEY, RDIO_SECRET))
NUMBER_OF_PEOPLE = 50

API_KEY = LAST_API_KEY 
API_SECRET = LAST_SECRET

username = LAST_USERNAME
password_hash = pylast.md5(LAST_PASSWORD)

network = pylast.LastFMNetwork(api_key = API_KEY, api_secret = 
    API_SECRET, username = username, password_hash = password_hash)
	
#Copy the [access_token] and enter it below

#token = 'CAAUz0srmPAUBAO8TtGGVCSNZCOFiCaZAhdz9MTD98jRCsPoknQMitXzsbMsLq5E0QKwkAOIVW0Fk6980A0jruAVCEM8Wl0GaCzFAhyM5prnZCdbS079FEYpITClf2GQwZBTsWKZB487mTir5yWSbsR4yhnOqqJmKFntCZABs9mRjRVjZBvvzxRdZBijaF5GAvZBiccQZAOMXtHogZDZD'
#Sets the authentication token

	
def find_artist_id(artist_name):
	x=rdio.call('search',params={'query': artist_name, 'types': 'Artist'})
	# results are returned in multiple layers of dictionaries and lists
	# the following lines extract the useful information
	y = x['result']
	z = y['results']
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
	x = rdio.call('getTracksForArtist',params={'artist': artistkey,'sort':'playCount','count':5})
	y = x['result']
	songlist = []
	for i in range(0,5):
		z = y[i]
		k = z['name']
		l = k[:46]
		songlist.append(l.replace("'","").encode('utf-8', errors='replace'))
	return songlist

def get_genre(artist):
	artist = network.get_artist(artist)
	topItems = artist.get_top_tags(limit=None)
	for topItem in topItems:
		return topItem.item.get_name().title().replace("'","").encode('utf-8', errors='replace')	

def get_artists(user_id, token):
	fb.set_access_token(token)
	dictionary = {}
	list = []
	dictionarylist = []
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
	b = Counter(list)
	i=0
	for artist in b:
		if b[artist] > (NUMBER_OF_PEOPLE/12):
			print artist, i
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
			i=i+1
	return dictionarylist
	
def format_text(list):
	f = open('sample.txt',"a")
	f.write('[\n')
	countcount=0
	for item in list:
		f.write('\t{\n')
		counter=0
		a=len(item)-1
		for key in item:
			if counter ==3:
				f.write("\t\t%r: [" % (key.encode('utf-8', errors='replace')))
				counter2=0
				for song in item["songs"]:
					f.write("\t\t{\"name\":%r}" % song)
					counter2=counter2+1
					if counter2==5:
						f.write("\n\t\t\t],\n")
						break
					f.write(",\n")
				counter=counter+1
			else:
				f.write("\t\t%r: %r" % (key.encode('utf-8', errors='replace')), item[key]))
				counter=counter+1
				if counter == 6:
					f.write("\n")
					break
				f.write(",\n")
		countcount=countcount+1
		if countcount<a:
			f.write('\t},\n')
		else:
			f.write('\t}\n')
	f.write(']')
	f.close()
	h = open('sample.txt','r')
	g = open('sample2.txt','w')
	for line in h:
		g.write(line.replace('\'', '"'))
	h.close()
	g.close()
	
	
def json_list(list):
	return json.dumps(list, sort_keys = True, indent = 4)

#f=open("sample.txt","w")
#format_text(get_artists('sebastian.rollen', token))
