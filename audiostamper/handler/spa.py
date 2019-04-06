import os

import tornado.web

from audiostamper.logic.analyse import audio_analyse, feature_analyse


class AppHandler(tornado.web.RequestHandler):
	SUPPORTED_METHODS = tornado.web.RequestHandler.SUPPORTED_METHODS

	async def get(self, *args, **kwargs):
		with open(os.path.join(self.application.build_dir, 'index.html'), 'r') as handler:
			self.write(handler.read())
