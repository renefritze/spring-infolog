# -*- coding: utf-8 -*-
from siteglobals import db
from backend import *
db.Connect()
db.metadata.drop_all()