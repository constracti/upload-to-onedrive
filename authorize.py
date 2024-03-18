#!/usr/bin/python3

import http.server

from class_installation import Installation
from class_server import Server

installation = Installation()

client = installation.get_client(v=True)

def write_refresh_token(refresh_token):
	installation.set_refresh_token(refresh_token)

server_name = 'localhost'
server_address = (server_name, 0)
server = http.server.HTTPServer(server_address, Server)
server_port = server.server_port
print('=== server url ===')
print('http://{:s}:{:d}/init'.format(server_name, server_port))
print()

print('Navigate to the page above and follow the instructions.')
print('To kill the server press Ctrl+C on this window.')
print()

server.client = client
server.callback = write_refresh_token
try:
	server.serve_forever()
except KeyboardInterrupt:
	print()
	server.server_close()
