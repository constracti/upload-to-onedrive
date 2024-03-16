#!/usr/bin/python3

import http.server
import json
import os.path

from server import UploadToOneDriveServer

script_path = os.path.abspath(__file__)
script_dir = os.path.dirname(script_path)

def read_client_secret():
	client_name = 'client_secret.json'
	client_path = os.path.join(script_dir, client_name)
	with open(client_path, 'r') as f:
		client = json.load(f)
	assert client is not None
	return client

def write_refresh_token(refresh_token):
	refresh_name = 'refresh_token.txt'
	refresh_path = os.path.join(script_dir, refresh_name)
	with open(refresh_path, mode='w') as f:
		f.write(refresh_token + '\n')

client = read_client_secret()

assert 'authorization_endpoint' in client
print('=== authorization endpoint ===')
print(client['authorization_endpoint'])
print()

assert 'token_endpoint' in client
print('=== token endpoint ===')
print(client['token_endpoint'])
print()

assert 'client_id' in client
print('=== client id ===')
print(client['client_id'])
print()

assert 'client_secret' in client
print('=== client secret ===')
print(client['client_secret'])
print()

address = ('localhost', 46579)
print('=== server url ===')
print('http://{:s}:{:d}/init'.format(*address))
print()

print('Navigate to the page above and follow the instructions.')
print('To kill the server press Ctrl+C on this window.')
print()

server = http.server.HTTPServer(address, UploadToOneDriveServer)
server.client = client
server.callback = write_refresh_token
try:
	server.serve_forever()
except KeyboardInterrupt:
	print()
	server.server_close()
