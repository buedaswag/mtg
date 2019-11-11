#! /home/mig/anaconda3/envs/mtg/bin/python

import logging
import sys
logging.basicConfig(stream=sys.stderr)
sys.path.append('/home/mig/mtg/app/app/')
from app.app.flask_app import app as application
