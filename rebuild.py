#!/usr/bin/env python
# -*- coding: utf-8 -*-
from siteglobals import db
from backend import *
db.Connect()
db.metadata.drop_all()
db.metadata.create_all()