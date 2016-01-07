#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from flask.ext.sqlalchemy import SQLAlchemy

db = SQLAlchemy()

from .user import *
from .notice import *
from .order import *
from .shoplog import *
from .mailbox import *