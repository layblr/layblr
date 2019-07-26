import json
import os
import tornado.web

from layblr.logic.importer import import_predictions


class ImporterHandler(tornado.web.RequestHandler):
	SUPPORTED_METHODS = tornado.web.RequestHandler.SUPPORTED_METHODS
	REQUIRED_KEYS = [
		'audioFile', 'predictionsFile'
	]

	async def post(self, *args, **kwargs):
		try:
			data = json.loads(self.request.body)  # type: dict
		except:
			return self.send_error(status_code=400)

		if not all(k in data for k in self.REQUIRED_KEYS):
			return self.send_error(status_code=400)

		audio_file = data['audioFile']
		audio_path = os.path.join(self.application.root_dir, os.path.basename(audio_file))
		prediction_file = data['predictionsFile']
		prediction_path = os.path.join(self.application.root_dir, os.path.basename(prediction_file))
		options = dict(
			audio_file=audio_file, audio_path=audio_path,
			prediction_file=prediction_file, prediction_path=prediction_path,
		)

		# Call the logic.
		try:
			results = await import_predictions(**options)
		except Exception as e:
			print(e)
			print(str(e))
			return self.send_error(status_code=500)

		return self.write(results)
