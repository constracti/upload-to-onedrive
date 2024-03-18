#!/usr/bin/python3

import argparse
import mimetypes
import os.path
import requests

from class_installation import Installation

parser = argparse.ArgumentParser()
parser.add_argument('file', metavar='FILE')
args = parser.parse_args()

file_path = args.file

installation = Installation()

access_token = installation.get_access_token()

file_name = os.path.basename(file_path)
file_size = os.path.getsize(file_path)
file_mime_type = mimetypes.guess_type(file_path)[0]

file_obj = open(file_path, 'rb')
url = 'https://graph.microsoft.com/v1.0/me/drive/root:/{:s}:/content'.format(file_name)
r = requests.put(url, headers={
	'Authorization': 'Bearer ' + access_token,
	'Content-Type': file_mime_type,
}, data=file_obj.read())
r = r.json()
assert 'error' not in r, r['error']['message']
file_obj.close()

print(r['id'])
