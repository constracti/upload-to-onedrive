import http.server
import requests
import urllib.parse


from page import UploadToOnedrivePage


class UploadToOnedriveServer(http.server.BaseHTTPRequestHandler):

	def get_addr(self, path='/'):
		return 'http://{:s}:{:d}{:s}'.format(self.server.server_name, self.server.server_port, path)

	def get_client(self):
		return self.server.client

	def get_auth_url(self):
		return self.get_client()['authorization_endpoint'] + '?' + urllib.parse.urlencode({
			'client_id': self.get_client()['client_id'],
			'scope': 'offline_access files.readwrite',
			'redirect_uri': self.get_addr('/auth'),
			'response_type': 'code',
		})

	def get_exch_url(self):
		return self.get_client()['token_endpoint']

	def get_exch_data(self, code):
		return {
			'client_id': self.get_client()['client_id'],
			'redirect_uri': self.get_addr('/auth'),
			'client_secret': self.get_client()['client_secret'],
			'code': code,
			'grant_type': 'authorization_code',
		}

	def redirect(self, url):
		self.send_response(307)
		self.send_header('Location', url)
		self.end_headers()

	def alert(self, message):
		page = UploadToOnedrivePage()
		page.add_body_tag('<p>{:s}</p>'.format(message))
		html = page.get_html()
		self.send_response(200)
		self.send_header('Content-Type', 'text/html')
		self.end_headers()
		self.wfile.write(bytes(html, 'utf-8'))

	def do_GET(self):
		path = urllib.parse.urlparse(self.path)
		try:
			if path.path == '/init':
				self.redirect(self.get_auth_url())
				# TODO revoke user consent
			elif path.path == '/auth':
				query = urllib.parse.parse_qs(path.query, True)
				assert 'error' not in query, query['error_description'][0]
				code = query['code'][0]
				r = requests.post(self.get_exch_url(), data=self.get_exch_data(code))
				r = r.json()
				assert 'error' not in r, r['error_description']
				refresh_token = r['refresh_token']
				self.server.callback(refresh_token)
				self.redirect(self.get_addr('/over'))
			elif path.path == '/over':
				self.alert('Close this tab. Then return to the application and press Ctrl+C.')
		except Exception as e:
			error = str(e)
			self.log_error(error)
			self.alert('Error: {:s}</p>\n'.format(error))
