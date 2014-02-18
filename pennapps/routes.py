# -*- coding: utf-8 -*-
import os, sys
from pennapps import app
from flask import render_template, send_from_directory, url_for, session, redirect, request, Response
from models import db, Member
from flask_oauth import OAuth
from fb_api import get_artists, format_text, FACEBOOK_APP_ID, FACEBOOK_SECRET_KEY
import json

@app.route('/')
def index():
  return render_template('partials/home.html') 


oauth = OAuth()

facebook = oauth.remote_app('facebook',
    base_url='https://graph.facebook.com/',
    request_token_url=None,
    access_token_url='/oauth/access_token',
    authorize_url='https://www.facebook.com/dialog/oauth',
    consumer_key=FACEBOOK_APP_ID,
    consumer_secret=FACEBOOK_SECRET_KEY,
    request_token_params={'scope': ('email, user_friends, friends_likes, friends_events, user_events, user_likes')}
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
    next_url = request.args.get('next') or url_for('jukify')
    if resp is None or 'access_token' not in resp:
        return redirect(next_url)
    session['logged_in'] = True
    session['facebook_token'] = (resp['access_token'], '')
    return redirect(next_url)

@app.route("/logout")
def logout():
    pop_login_session()
    return redirect(url_for('index'))

@app.route("/phones/phones.json")
def playlist():
  asciitoken = session['facebook_token'][0]
  response.headers['Access-Control-Allow-Origin'] = "*"
  return Response(response=format_text(get_artists(asciitoken.encode('utf-8'))), headers={'Access-Control-Allow-Origin' : "*"})

@app.route("/jukify")
def jukify():
  data = facebook.get('/me').data
  if 'id' in data and 'name' in data:
    return render_template('partials/phone-list.html') 
  return redirect(url_for('index'))
