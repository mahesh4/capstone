#!/usr/bin/env python

import webapp2
import os
import jinja2
import re
import logging
import urllib2
import time
import json
from google.appengine.api import memcache

url = "http://ec2-35-154-245-161.ap-south-1.compute.amazonaws.com/data"
template_dir = os.path.join(os.path.dirname(__file__),'templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir),
							   autoescape=True)

class Handler(webapp2.RequestHandler):
	def json_write(self,data):
		self.response.headers['Content-Type'] = 'application/json' 
		self.response.out.write(json.dumps(data))

		
class HomeHandler(Handler):
	def get(self):
		self.response.out.write("use post request")
	def post(self):
		req = json.loads(self.request.body)
		lane_data = self.get_lane_data()
		if lane_data is None:
			result = {"displayText":"data seems to be unavailable right now, try again later","speech":"data seems to be unavailable right now, try again later",}
		else:
			keys = req['result']['parameters']['traffic-lane']
			if 'all' in keys:
				speech = ". ".join(["%s has %s vehicles" % (l,lane_data[l]) for l in lane_data.keys()])
			else:
				speech = ". ".join(["%s has %s vehicles" % (l,lane_data[l]) for l in keys])
			result = {"displayText":speech,"speech":speech,}
		self.json_write(result)
	def get_lane_data(self):
		data = urllib2.urlopen(url)
		data = data.read()
		if data == 'null':
			return None
		else:
			return json.loads(data)


app = webapp2.WSGIApplication([
		('/',HomeHandler), ],debug=True)
