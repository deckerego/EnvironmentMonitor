#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import logging

logging.basicConfig(level=logging.WARN, format='%(levelname)-8s %(message)s')
logger = logging.getLogger('sprinkerswitch')

os.chdir(os.path.dirname(__file__))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), ".")))

import json
import time
import datetime
from piwiring import GPIO
from HIH6130 import Temperature
from noaa import Forecast
from jabber import Jabber
from config import configuration
from bottle import Bottle, HTTPResponse, static_file, get, put, request, response, template

instance_name = configuration.get('instance_name')

temperature = Temperature()
gpio = GPIO()
forecast = Forecast()
jabber_service = Jabber(configuration.get('xmpp_username'), configuration.get('xmpp_password'), temperature, gpio)

application = Bottle()
application.install(temperature)
application.install(gpio)
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

@application.get('/')
def dashboard():
	return template('index', webcam_url=configuration.get('webcam_url'))

@application.get('/environment')
def get_environment(temperature):
	humidity, celsius, status = temperature.get_conditions()
	fahrenheit_val = ((celsius * 9) / 5) + 32 if celsius else "null"
	celsius_val = celsius if celsius else "null"
	humidity_val = humidity if humidity else "null"
	status_val = status if status else "null"
	return '{ "relative_humidity": %s, "celsius": %s, "fahrenheit": %s, "status": %s }' % (humidity_val, celsius_val, fahrenheit_val, status_val)

@application.get('/forecast/temperature')
def get_temperature(forecast):
	temperatures = {}
	starttimes, hourlys = zip(*forecast.temperature())
	temperatures['lastUpdated'] = forecast.last_updated()
	temperatures['times'] = starttimes
	temperatures['hourly'] = hourlys
	return json.dumps(temperatures)

@application.get('/forecast/apparentTemp')
def get_apparent_temperature(forecast):
	temperatures = {}
	starttimes, hourlys = zip(*forecast.apparent_temperature())
	temperatures['lastUpdated'] = forecast.last_updated()
	temperatures['times'] = starttimes
	temperatures['apparentTemperature'] = hourlys
	return json.dumps(temperatures)

@application.get('/forecast/dewpoint')
def get_dewpoint(forecast):
	temperatures = {}
	starttimes, dewpoints = zip(*forecast.dewpoint())
	temperatures['lastUpdated'] = forecast.last_updated()
	temperatures['times'] = starttimes
	temperatures['dewpoints'] = dewpoints
	return json.dumps(temperatures)

@application.get('/forecast/precipitation')
def get_precipitation(forecast):
	precips = {}
	starttimes, precipitation = zip(*forecast.precipitation())
	precips['lastUpdated'] = forecast.last_updated()
	precips['times'] = starttimes
	precips['inches'] = precipitation
	return json.dumps(precips)

@application.get('/forecast/wind')
def get_wind(forecast):
	winds = {}
	starttimes, speeds, directions = zip(*forecast.wind())
	winds['lastUpdated'] = forecast.last_updated()
	winds['times'] = starttimes
	winds['speed'] = speeds
	winds['direction'] = directions
	return json.dumps(winds)

@application.get('/forecast/cloudcover')
def get_cloudcover(forecast):
	clouds = {}
	starttimes, coverages = zip(*forecast.cloudcover())
	clouds['lastUpdated'] = forecast.last_updated()
	clouds['times'] = starttimes
	clouds['percentage'] = coverages
	return json.dumps(clouds)

@application.get('/forecast/humidity')
def get_humidity(forecast):
	humidity = {}
	starttimes, relative_humidity = zip(*forecast.humidity())
	humidity['lastUpdated'] = forecast.last_updated()
	humidity['times'] = starttimes
	humidity['relativeHumidity'] = relative_humidity
	return json.dumps(humidity)

@application.put('/forecast/update')
def update_forecast(forecast):
	forecast.update()
	return '{ "lastUpdated": "%s" }' % forecast.last_updated()

@application.get('/switch/<button:int>')
def get_switch_status(button, gpio):
	return '{ "enabled": %s }' % ("true" if gpio.is_enabled(button) else "false")

@application.put('/switch/<button:int>')
def set_switch_status(button, gpio):
	if request.json['enabled']:
		gpio.enable(button)
		logging.info("Switch %d ON" % button)
	else:
		gpio.disable(button)
		logging.info("Switch %d OFF" % button)
	return get_switch_status(button, gpio)
