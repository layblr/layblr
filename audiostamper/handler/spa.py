import os
from typing import Optional

import tornado.web

from audiostamper.logic.analyse import audio_analyse, feature_analyse


class AppHandler(tornado.web.StaticFileHandler):
	def validate_absolute_path(self, root: str, absolute_path: str) -> Optional[str]:
		try:
			return super().validate_absolute_path(root, absolute_path)
		except tornado.web.HTTPError as e:
			if e.status_code == 404:
				return super().validate_absolute_path(
					root, os.path.join(self.application.build_dir, 'index.html')
				)
			raise e
