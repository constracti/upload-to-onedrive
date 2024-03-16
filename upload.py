#!/usr/bin/python3

import os.path
import json
import requests

script_path = os.path.abspath(__file__)
script_dir = os.path.dirname(script_path)

def read_client_secret():
	client_name = 'client_secret.json'
	client_path = os.path.join(script_dir, client_name)
	with open(client_path, 'r') as f:
		client = json.load(f)
	assert client is not None
	return client

client = read_client_secret()

assert 'token_endpoint' in client
print('=== token endpoint ===')
print(client['token_endpoint'])
print()

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

refresh_token = None
refresh_name = 'refresh_token.txt'
refresh_path = os.path.join(script_dir, refresh_name)
with open(refresh_path, mode='r') as f:
	refresh_token = f.read().rstrip()

print('=== refresh token ===')
print(refresh_token)
print()

r = requests.post(client['token_endpoint'], data={
	'client_id': client['client_id'],
	'client_secret': client['client_secret'],
	'refresh_token': refresh_token,
	'grant_type': 'refresh_token',
})
r = r.json()
assert 'error' not in r, r['error_description']
access_token = r['access_token']

print('=== access token ===')
print(access_token)
print()

r = requests.put('https://graph.microsoft.com/v1.0/me/drive/root:/myfile.txt:/content', headers={
	'Authorization': 'Bearer ' + access_token,
	'Content-Type': 'text/plain',
}, data='The contents of the file goes here.')
r = r.json()
assert 'error' not in r, '{} - {}'.format(r['error']['code'], r['error']['message'])

print(r['id'])
