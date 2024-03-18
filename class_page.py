class Page:

	def __init__(self, title='Upload to OneDrive'):
		self.title = title
		self.body_tags = []

	def add_body_tag(self, tag):
		self.body_tags.append(tag)

	def get_html(self):
		html = '<html>\n'
		html += '<head>\n'
		html += '<title>{:s}</title>\n'.format(self.title) # TODO escape html
		html += '</head>\n'
		html += '<body>\n'
		html += '<h1>{:s}</h1>\n'.format(self.title) # TODO escape html
		for tag in self.body_tags:
			html += tag
		html += '</body>\n'
		html += '</html>\n'
		return html
