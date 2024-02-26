#!/usr/bin/python3
"""Blueprint initialization."""

from flask import Blueprint
from .amenities import *
from .cities import *
from .index import *
from .places import *
from .places_reviews import *
from .states import *
from .users import *

app_views = Blueprint("app_views", __name__, url_prefix="/api/v1")
