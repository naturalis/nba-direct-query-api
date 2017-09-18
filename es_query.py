import sys
import requests
import json
from flask import Flask
from flask import request, make_response, render_template
from os import environ

app = Flask(__name__)

try:
	ip = environ['ES_ADDRESS']
	port = environ['ES_PORT']
except Exception as e:
	print('no environs found')
	print(e)
	exit(1)

try:
	es_request_timeout = int(environ['ES_TIMEOUT'])
except Exception as e:
	es_request_timeout = 10

base_url = 'http://' + ip + ':' + port
services = ['taxon','specimen','multimedia','geo','storageunits']

@app.route('/')
def root():
	response = make_response(render_template('info.txt',services=services,base_url=base_url))
	response.headers['content-type'] = 'text/plain'
	return response

@app.route('/<service>/', methods=['GET','POST'])
def query(service):
	if not service in services:
		return 'unknown service %s' % service

	if request.method == 'POST':
		query=request.form['query']
	else:
		query=request.args.get('query', '')

	if len(query.strip())==0:
		return 'no query'
		
	try:
		r = requests.post(base_url+'/'+service+'/_search',data=query,timeout=es_request_timeout)
		response = make_response(r.content)
		response.headers['content-type'] = 'application/json; charset=utf-8'
		return response	
	except Exception as e:
		return 'request error: ' + str(e)
		
if __name__ == "__main__":
	app.run(host="0.0.0.0")
