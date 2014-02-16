#!/usr/bin/python
# -*- coding: utf-8 -*-

from werkzeug import generate_password_hash, check_password_hash
from flask.ext.sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Member(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(50))
