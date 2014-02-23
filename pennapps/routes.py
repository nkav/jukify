# -*- coding: utf-8 -*-
import os, sys
from pennapps import app
from flask import render_template, send_from_directory, url_for, session, redirect, request, Response
from models import db, Member
from flask_oauth import OAuth
from forms import EventForm
from fb_api import run_all, FACEBOOK_APP_ID, FACEBOOK_SECRET_KEY
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
    next_url = request.args.get('next') or url_for('eventform')
    if resp is None or 'access_token' not in resp:
        return redirect(next_url)
    session['logged_in'] = True
    session['facebook_token'] = (resp['access_token'], '')
    return redirect(next_url)

@app.route("/logout")
def logout():
    pop_login_session()
    return redirect(url_for('index'))

@app.route("/acctoken")
def token():
	sys.stderr.write("\nTHIS IS THE TYPE %s\n" % type(session['facebook_token'][0].encode('utf-8')))
	return session['facebook_token'][0]

@app.route("/eventform", methods=['GET', 'POST'])
def eventform():
	form = EventForm()
	if form.validate_on_submit():
		session['eventurl'] = form.url.data
		return redirect(url_for('playlist'))
	return render_template('partials/eventform.html', form=form)

@app.route("/phones")
def playlist():
	if 'eventurl' not in session:
		return redirect(url_for('eventform'))
	eventurl = str(session['eventurl'])
	asciitoken = session['facebook_token'][0]
	#sys.stderr.write(str(type(session['facebook_token'][0].encode('utf-8'))))
	#sys.stderr.write(str(session['facebook_token'][0].encode('utf-8')))
	#sys.stderr.write(str(type(eventurl)))
	return Response(response=run_all(eventurl, asciitoken.encode('utf-8')), headers={'Access-Control-Allow-Origin' : "*"})
	#return Response(response=run_all(eventurl, "CAADH7BdddM0BAAel3FiQCSDKpVEJRrZC4r1mij8uNkxUReqY06fQUJdkIipPD3eTCadduSb4zKgL7FxwZBlO9L9kKdrCfcASJ9kZBsS20sVoYAuyciSfPH6tBm6bdZAKhodqa2USdwK2gAaKFWLmQUOkQE6vvT3lTGrCeZArcUWStoDdm2S57uJ0zlFkSrPoZD"), headers={'Access-Control-Allow-Origin' : "*"})

@app.route("/jukify")
def jukify():
  data = facebook.get('/me').data
  if 'id' in data and 'name' in data:
    return render_template('partials/phone-list.html') 
  return redirect(url_for('index'))
