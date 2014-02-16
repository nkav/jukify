#!/usr/bin/python
# -*- coding: utf-8 -*-
<<<<<<< HEAD
from pennapps import app
from flask import render_template, request, flash, session, url_for, redirect, send_from_directory
from models import db, Member

@app.route('/')
def home():
  return "Hello, world!" 

@app.route('/home')
def hello():
  return "Hello world!"

import os, sys
from pennapps import app
from flask import render_template, send_from_directory, url_for, session, redirect, request
from models import db, Member
from settings import FACEBOOK_APP_ID, FACEBOOK_APP_SECRET 
from flask_oauth import OAuth
from fb_api import get_artists
import json

@app.route('/')
def index():
  return "Hello, world!" 

oauth = OAuth()

facebook = oauth.remote_app('facebook',
    base_url='https://graph.facebook.com/',
    request_token_url=None,
    access_token_url='/oauth/access_token',
    authorize_url='https://www.facebook.com/dialog/oauth',
    consumer_key=FACEBOOK_APP_ID,
    consumer_secret=FACEBOOK_APP_SECRET,
    request_token_params={'scope': ('email, ')}
)

@facebook.tokengetter
def get_facebook_token():
    return session.get('facebook_token')

def pop_login_session():
    session.pop('logged_in', None)
    session.pop('facebook_token', None)

@app.route("/facebook_login")
def facebook_login():
    return facebook.authorize(callback=url_for('facebook_authorized',
        next=request.args.get('next'), _external=True))

@app.route("/facebook_authorized")
@facebook.authorized_handler
def facebook_authorized(resp):
    next_url = request.args.get('next') or url_for('index')
    if resp is None or 'access_token' not in resp:
        return redirect(next_url)
    session['logged_in'] = True
    session['facebook_token'] = (resp['access_token'], '')
    return redirect(next_url)

@app.route("/logout")
def logout():
    pop_login_session()
    return redirect(url_for('index'))

@app.route("/findfriends")
def findfriends():
  data = facebook.get('/me').data
  if 'id' in data and 'name' in data:
    user_id = data['id']
    user_name = data['name']
    asciitoken = session['facebook_token'][0]
    songs = get_artists("sebastian.rollen", asciitoken.encode('utf-8', errors='replace'))
    return str(type(songs))
    # songlist = [str(song) for song in songs]	
    #stringrep = '\n'.join(songlist)
    #return stringrep 
  return "Nope"
