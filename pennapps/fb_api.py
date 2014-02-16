# -*- coding: utf-8 -*-
from pyfb import Pyfb
from settings import FACEBOOK_APP_ID, FACEBOOK_SECRET_KEY, RDIO_KEY, RDIO_SECRET
import sys
from collections import Counter
import json
from rdio import Rdio

fb = Pyfb(FACEBOOK_APP_ID)
rdio = Rdio((RDIO_KEY, RDIO_SECRET))

#Copy the [access_token] and enter it below

token = 'CAAUz0srmPAUBAAVpXbhH36G3CZBHlWqY95va4nRemDL7cglgdVkhKDOLoptlZBe5KuXKZB37xMtztCxcPttK2qhXzVoYYSrHPTn3Uykr10axK11SZCrlbdnH2HbswtpZAQLrbr6qB0YmdNrJ0DX8cAaEE7EbEPt6fub8KfttXplsA0cMkjode0GoGaQ6PKDjYp0cBq1o5rgZDZD'
#Sets the authentication token
fb.set_access_token(token)
	
def find_artist_id(artist_name):
	x=rdio.call('search',params={'query': artist_name, 'types': 'Artist'})
	# results are returned in multiple layers of dictionaries and lists
	# the following lines extract the useful information
	y = x['result']
	z = y['results']
	q = z[0]
	w = q['key'].encode(sys.stdout.encoding, errors='replace')
	return w
	
def find_artist_image(artist):
	artistkey = find_artist_id(artist)
	x = rdio.call('getTracksForArtist',params={'artist': artistkey,'sort':'playCount','count':5})
	y = x['result']
	z = y[0]
	c = z['icon'].encode(sys.stdout.encoding, errors='replace')
	return c
	
def find_songs(artist):
	artistkey = find_artist_id(artist)
	x = rdio.call('getTracksForArtist',params={'artist': artistkey,'sort':'playCount','count':5})
	y = x['result']
	songlist = []
	for i in range(0,5):
		z = y[i]
		songlist.append(z['name'].encode(sys.stdout.encoding, errors='replace'))
	return songlist
	
def get_artists(user_id):
	dictionary = {}
	list = []
	dictionarylist = []
	i = 0
	friends = fb.get_friends(user_id)
	for friend in friends:
		if i < 50:
			a = fb.get_likes(friend.id)
			while (a):
				for like in a:
					if like.category == "Musician/band":
						 list.append(like.name.encode(sys.stdout.encoding, errors='ignore'))
				a = a.next()
			i = i + 1
			print friend.name +" %d" % i
	b = Counter(list)
	i=0
	for artist in b:
		if b[artist] > 4:
			dictionary["likes"] = b[artist]
			dictionary["name"] = artist
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
			dictionarylist.append(dictionary.copy())
			i=i+1
			print i
	return dictionarylist
	
def format_text(list):
	f = open('sample.txt',"a")
	f.write('[\n')
	for item in list:
		f.write('\t{\n')
		counter=0
		for key in item:
			f.write("\t\t%r: %r" % (key.encode(sys.stdout.encoding, errors='replace'), item[key]))
			counter=counter+1
			if counter == 5:
				f.write("\n")
				break
			f.write(",\n")
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
	
	
#print json_list(get_artists('sebastian.rollen'))
