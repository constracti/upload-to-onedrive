class UploadToOnedrivePage:

	def __init__(self):
		self.body_tags = []

	def add_body_tag(self, tag):
		self.body_tags.append(tag)

	def get_html(self):
		html = '<html>\n'
		html += '<head>\n'
		html += '<title>Upload to Onedrive</title>\n'
		html += '</head>\n'
		html += '<body>\n'
		html += '<h1>Upload to Onedrive</h1>\n'
		for tag in self.body_tags:
			html += tag
		html += '</body>\n'
		html += '</html>\n'
		return html
