#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
	Dump flask-based http proxy.
	Get habrahabr link and return html content with ™ symbol added to every
	six letters word.
	Version 0.1
	Usage: type in cli 
	$python3 proxy.py
	and open link http://127.0.0.1:5000/post/320476/
"""

import requests
import string
import os

from flask import Flask, Response
from flask import stream_with_context, send_from_directory

from bs4 import BeautifulSoup

site_name = 'http://habrahabr.ru/'

app = Flask(__name__)


def is_in(s):
	"""Return 1 if the string contains at least one punctuation symbol"""
	is_p = 0
	for i in s:
		if i in string.punctuation:
			is_p = 1
			break
	return is_p


@app.route('/favicon.ico')
def favicon():
	"""Favicon request handler"""
	return send_from_directory(
		os.path.join(app.root_path, 'static'),
		'favicon.ico', mimetype='image/favicon.ico')


@app.route('/<path:url>')
def home(url):
	req = requests.get(site_name + url, stream=True)
	soup = BeautifulSoup(req.text, 'lxml')
	post_content = soup.find('div', {'class': 'content html_format'})
	pc = post_content.get_text()
	plist = pc.split()
	print('Plist len', len(plist))

	for i in range(len(plist)):
			if len(plist[i]) == 6:
					if is_in(plist[i]) == 0:
						x = list(plist[i])
						x.append(u'\u2122')
						x = ''.join(x)
						plist[i] = x

	content_out = ' '.join(plist)

	return content_out

if __name__ == '__main__':
	app.run(debug=True)
