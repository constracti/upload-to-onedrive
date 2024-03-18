import os
import os.path
import json
import requests


class Installation:

	def __init__(self):
		self.cwd = os.getcwd()
		self.client = None
		self.refresh_token = None

	def get_client(self, v=False):
		if self.client is None:
			self.read_client(v)
		return self.client

	def read_client(self, v=False):
		client_name = 'client_secret.json'
		client_path = os.path.join(self.cwd, client_name)
		with open(client_path, 'r') as f:
			client = json.load(f)
		assert client is not None
		assert 'authorization_endpoint' in client
		assert 'token_endpoint' in client
		assert 'client_id' in client
		assert 'client_secret' in client
		if v:
			print('=== authorization endpoint ===')
			print(client['authorization_endpoint'])
			print()
		if v:
			print('=== token endpoint ===')
			print(client['token_endpoint'])
			print()
		if v:
			print('=== client id ===')
			print(client['client_id'])
			print()
		if v:
			print('=== client secret ===')
			print(client['client_secret'])
			print()
		self.client = client

	def get_refresh_token(self, v=False):
		if self.refresh_token is None:
			self.read_refresh_token(v)
		return self.refresh_token

	def read_refresh_token(self, v=False):
		refresh_token = None
		refresh_name = 'refresh_token.txt'
		refresh_path = os.path.join(self.cwd, refresh_name)
		with open(refresh_path, mode='r') as f:
			refresh_token = f.read().rstrip()
		if v:
			print('=== refresh token ===')
			print(refresh_token)
			print()
		self.refresh_token = refresh_token

	def set_refresh_token(self, refresh_token):
		refresh_name = 'refresh_token.txt'
		refresh_path = os.path.join(self.cwd, refresh_name)
		with open(refresh_path, mode='w') as f:
			f.write(refresh_token + '\n')
		self.refresh_token = refresh_token

	def get_access_token(self, v=False):
		client = self.get_client()
		refresh_token = self.get_refresh_token()
		r = requests.post(client['token_endpoint'], data={
			'client_id': client['client_id'],
			'client_secret': client['client_secret'],
			'refresh_token': refresh_token,
			'grant_type': 'refresh_token',
		})
		r = r.json()
		assert 'error' not in r, r['error_description']
		access_token = r['access_token']
		if v:
			print('=== access token ===')
			print(access_token)
			print()
		return access_token
