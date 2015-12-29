#!/usr/bin/env python
# -*- coding: UTF-8 -*-
from ._base import db
from .user import *
from .site import *


from flask.ext.sqlalchemy import SQLAlchemy

db = SQLAlchemy()
