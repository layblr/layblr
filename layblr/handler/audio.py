import os

import tornado.web

from layblr.logic.analyse import audio_analyse, feature_analyse


class AudioFileHandler(tornado.web.RequestHandler):
	SUPPORTED_METHODS = tornado.web.RequestHandler.SUPPORTED_METHODS
	CHUNK_SIZE = 512000  # 0.5 MB

	async def get(self, file_name, *args, **kwargs):
		root_dir = self.application.root_dir
		file_path = os.path.join(root_dir, os.path.basename(file_name))
		req_range = self.request.headers.get('Range', '')
		_, file_ext = file_path.rsplit('.', maxsplit=1)

		if not os.path.exists(file_path) or not os.path.isfile(file_path):
			raise tornado.web.HTTPError(404)

		if req_range != '':
			self.set_header('Range', req_range)

		# Set headers.
		self.set_header('Content-Type', 'audio/mpeg' if file_ext == 'mp3' else 'audio/wav')
		self.set_header('Content-Length', os.path.getsize(file_path))

		# Open and read the requested range.


		print(file_path)
		print(req_range)
		print(file_ext)

