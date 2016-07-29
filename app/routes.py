#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import logging

logging.basicConfig(level=logging.WARN, format='%(levelname)-8s %(message)s')
logger = logging.getLogger('environmon')

os.chdir(os.path.dirname(__file__))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), ".")))

import json
import time
import datetime
from HIH6130 import Temperature
from jabber import Jabber
from config import configuration
from bottle import Bottle, HTTPResponse, static_file, get, put, request, response, template

instance_name = configuration.get('instance_name')

temperature = Temperature()
jabber_service = Jabber(configuration.get('xmpp_username'), configuration.get('xmpp_password'), temperature, gpio)

application = Bottle()
application.install(temperature)
application.install(forecast)
#FIXME Right now two clients (like garagesec and sprinkler) can't co-exist
#application.install(jabber_service)

@application.route('/favicon.ico')
def send_favicon():
	return static_file('favicon.ico', root='views/images')

@application.route('/installed/<filename:path>')
def send_bower(filename):
	return static_file(filename, root='views/bower_components')

@application.route('/js/<filename:path>')
def send_js(filename):
	return static_file(filename, root='views/js')

@application.route('/css/<filename:path>')
def send_css(filename):
	return static_file(filename, root='views/css')
