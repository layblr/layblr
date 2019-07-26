import os

import tornado.web

from layblr.logic.analyse import audio_analyse, feature_analyse


class AnalyseHandler(tornado.web.RequestHandler):
	SUPPORTED_METHODS = tornado.web.RequestHandler.SUPPORTED_METHODS

	async def get(self, *args, **kwargs):
		root_dir = self.application.root_dir
		file_name = kwargs['file']
		file_path = os.path.join(root_dir, os.path.basename(file_name))
		if '.' not in file_name:
			self.send_error(status_code=400)
			return
		if not os.path.exists(file_path) or not os.path.isfile(file_path):
			self.send_error(status_code=404)
			return
		_, file_ext = file_name.rsplit('.', maxsplit=1)

		# Analyse based on the file type.
		if file_ext in ['mp3', 'wav']:
			result = await audio_analyse(file_path)
		elif file_ext in ['csv']:
			result = await feature_analyse(file_path)
		else:
			result = None

		self.add_header('Content-Type', 'application/json')
		self.write(dict(
			file=file_name,
			result=result
		))
