import os

import tornado.web
from jinja2.filters import do_filesizeformat


class BrowserHandler(tornado.web.RequestHandler):
	SUPPORTED_METHODS = tornado.web.RequestHandler.SUPPORTED_METHODS

	def set_default_headers(self):
		# TODO: Remove in production.
		self.set_header("Access-Control-Allow-Origin", "*")
		self.set_header("Access-Control-Allow-Headers", "x-requested-with")
		self.set_header('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE, OPTIONS')

	def get(self, *args, **kwargs):
		root_dir = self.application.root_dir
		dir_list = os.listdir(root_dir)
		browse_type = self.request.query_arguments.get('type')
		if browse_type:
			browse_type = browse_type[0].decode()
		if not browse_type or browse_type not in ['audio', 'features', 'predictions']:
			browse_type = 'audio'

		# Filter based on the requested type.
		ext_filter = []
		if browse_type == 'audio':
			ext_filter += ['wav']
		elif browse_type == 'features' or browse_type == 'predictions':
			ext_filter += ['csv']

		# Get files.
		files = list()
		for filename in dir_list:
			file_path = os.path.join(root_dir, filename)
			if os.path.isdir(file_path) or '.' not in filename or filename.startswith('.'):
				continue
			else:
				_, file_ext = filename.rsplit('.', maxsplit=1)
				if file_ext not in ext_filter:
					continue

			stat = os.stat(file_path)
			files.append(dict(
				path=file_path,
				name=filename,
				size=stat.st_size,
				human_size=do_filesizeformat(stat.st_size),
				extension=file_ext,
			))

		self.add_header('Content-Type', 'application/json')
		self.write(dict(
			files=files
		))
