#!/usr/bin/python3

import argparse
import mimetypes
import os.path
import requests

from class_installation import Installation

parser = argparse.ArgumentParser()
parser.add_argument('file', metavar='FILE')
parser.add_argument('--path', metavar='PATH', default='')
parser.add_argument('--block-limit', type=int, default=320*1024)
args = parser.parse_args()

file_path = args.file
drive_path = args.path
block_lim = args.block_limit
assert block_lim > 0

installation = Installation()

access_token = installation.get_access_token()

file_name = os.path.basename(file_path)
file_size = os.path.getsize(file_path)
file_mime_type = mimetypes.guess_type(file_path)[0]

file_obj = open(file_path, 'rb')
url = 'https://graph.microsoft.com/v1.0/me/drive/root:/{:s}:/createUploadSession'.format(drive_path + file_name)
r = requests.post(url, headers={
	'Authorization': 'Bearer ' + access_token,
	'Content-Type': file_mime_type,
})
r = r.json()
assert 'error' not in r, r['error']['message']
upload_url = r['uploadUrl']

block_pos = 0
while True:
	block_data = file_obj.read(block_lim)
	block_size = len(block_data)
	if block_size == 0:
		break
	print('Upload {:.0f}%'.format(block_pos * 100. / file_size))
	block_beg = block_pos
	block_end = block_pos + block_size - 1
	block_pos += block_size
	# sometimes response.status_code is 503
	for attempt in range(10):
		r = requests.put(upload_url, headers={
			'Content-Length': '{:d}'.format(block_size),
			'Content-Range': 'bytes {:d}-{:d}/{:d}'.format(block_beg, block_end, file_size),
		}, data=block_data)
		if r.ok:
			break
	r = r.json()
	assert 'error' not in r, r['error']['message']
print('Upload complete')
file_obj.close()

print(r['id'])
