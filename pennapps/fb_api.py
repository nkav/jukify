
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

token = 'CAAUz0srmPAUBACxhcAPvQo57ayhBHrBb7ZC15DZAl5UZAfmbmkAQP4wTxRJ8w9OLBCzOYMe7ZAPSjQ3ZAK5wDFKGKrW4Pj4ER4sEFrgNZANHz3JxIqQ2C4ybnizQW8ObaSU1Tf6vm1EvMfi4sl1FznXLDZCSmEl0EK6k1ZBFr78yxLBQ62JSj4HuK92hZCIFuYPkgVNdljRfJnAZDZD'
#Sets the authentication token

	
def find_artist_id(artist_name):
	artistname = artist_name.encode('ascii', errors='replace')
	x=rdio.call('search',params={'query': artist_name, 'types': 'Artist'})
	# results are returned in multiple layers of dictionaries and lists
	# the following lines extract the useful information
	y = x['result']
	z = y['results']
	q = z[0]
	w = q['key'].encode('ascii', errors='replace')
	return w
	

def find_artist_image(artist):
	artistkey = find_artist_id(artist)
	x = rdio.call('getTracksForArtist',params={'artist': artistkey,'sort':'playCount','count':5})
	y = x['result']
	z = y[0]
	c = z['icon'].encode('ascii', errors='replace')
	return c
	
def find_songs(artist):
	artistkey = find_artist_id(artist)
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
		songlist.append(l.replace("'","").encode('ascii', errors='replace'))
	return songlist

def get_genre(artist):
	artist = network.get_artist(artist)
	topItems = artist.get_top_tags(limit=None)
	for topItem in topItems:
		a = topItem.item.get_name().title().replace("'","").encode('ascii', errors='replace')
		if a in ['Pop', 'House', 'Classical', 'Jazz', 'Country', 'Hip-Hop', 'Rock', 'Reggae']:
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
						 list.append(like.name.encode('ascii', errors='replace'))
				a = a.next()
			i = i + 1
			print friend.name.encode('ascii', errors='replace') +" %d" % i
	b = Counter(list)
	i=0
	for artist in b:
		if b[artist] > (NUMBER_OF_PEOPLE/20):
			if find_songs(artist) == []:
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
			i=i+1
			print artist, i
	return dictionarylist
	
def format_text(list):
	s=""
	s+=('[\n')
	countcount=1
	for item in list:
		s+=('\t{\n')
		counter=0
		a=len(item)-1
		for key in item:
			if counter ==3:
				s+=("\t\t%r: [" % (key.encode('ascii', errors='replace')))
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
				s+=("\t\t%r: %r" % (key.encode('ascii', errors='replace'), item[key]))
				counter=counter+1
				if counter == 6:
					s+=("\n")
					break
				s+=(",\n")
		countcount=countcount+1
		print countcount
		print a
		if countcount<a:
			s+=('\t},\n')
		else:
			s+=('\t}\n')
	s+=(']')
	return s
	
	
#def json_list(list):
#	return json.dumps(list, sort_keys = True, indent = 4)

#f=open("sample.txt","w")
print format_text(get_artists('sebastian.rollen', token))