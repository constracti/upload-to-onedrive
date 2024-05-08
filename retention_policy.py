#!/usr/bin/python3

import argparse
import datetime
import requests

from class_installation import Installation

parser = argparse.ArgumentParser()
parser.add_argument('path', metavar='PATH')
parser.add_argument('--days', metavar='DAYS', type=int, default=7)
args = parser.parse_args()

drive_path = args.path
days = args.days
assert days >= 0

installation = Installation()

access_token = installation.get_access_token()

url = 'https://graph.microsoft.com/v1.0/me/drive/root:/{:s}:/children?select=id,name,createdDateTime'.format(drive_path)
r = requests.get(url, headers={
	'Authorization': 'Bearer ' + access_token,
})
r = r.json()
assert 'error' not in r, r['error']['message']

for item in r['value']:
	date = datetime.datetime.strptime(item['createdDateTime'], '%Y-%m-%dT%H:%M:%SZ').date()
	if date <= datetime.date.today() - datetime.timedelta(days=days):
		print('Deleting', item['name'])
		url = 'https://graph.microsoft.com/v1.0/me/drive/items/{:s}/permanentDelete'.format(item['id'])
		r = requests.post(url, headers={
			'Authorization': 'Bearer ' + access_token,
		})
		assert r.status_code == 204, r.json()['error']['message']
