#! /home/mig/anaconda3/envs/mtg/bin/python

import logging
import sys
logging.basicConfig(stream=sys.stderr)
sys.path.insert(0, '~/mtg/app/')
from app import app as application
