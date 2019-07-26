import json
import os
import tornado.web

from layblr.logic import export


class ExportHandler(tornado.web.RequestHandler):
	SUPPORTED_METHODS = tornado.web.RequestHandler.SUPPORTED_METHODS
	REQUIRED_KEYS = [
		'audioFile', 'featuresFile', 'exportType', 'exportFile', 'sampleRate', 'totalDuration', 'totalSplits',
		'splitDuration', 'classifyCategories', 'frames',
	]
	POSSIBLE_TYPES = [
		'classified_features', 'separate_classes_per_split', 'separate_classes_per_frame'
	]

	def post(self, *args, **kwargs):
		try:
			data = json.loads(self.request.body)  # type: dict
		except:
			return self.send_error(status_code=400)

		if not all(k in data for k in self.REQUIRED_KEYS):
			return self.send_error(status_code=400)
		if not data['exportType'] in self.POSSIBLE_TYPES:
			return self.send_error(status_code=400)

		audio_file = data['audioFile']
		audio_path = os.path.join(self.application.root_dir, os.path.basename(audio_file))
		features_file = data['featuresFile']
		features_path = os.path.join(self.application.root_dir, os.path.basename(features_file))
		export_type = data['exportType']
		export_file = data['exportFile']
		export_path = os.path.join(self.application.root_dir, os.path.basename(export_file))
		sample_rate = data['sampleRate']
		total_duration = data['totalDuration']
		total_splits = data['totalSplits']
		split_duration = data['splitDuration']
		classify_categories = data['classifyCategories']
		frames = data['frames']
		options = dict(
			audio_file=audio_file, audio_path=audio_path, features_file=features_file, features_path=features_path,
			export_type=export_type, export_file=export_file, export_path=export_path, sample_rate=sample_rate,
			total_duration=total_duration, total_splits=total_splits, split_duration=split_duration,
			classify_categories=classify_categories, frames=frames
		)

		# Check if file already exist, if so, send '409 Conflict' to the client.
		if os.path.exists(export_path):
			return self.send_error(status_code=409)

		# Call the correct exporter.
		method_name = 'export_{}'.format(export_type)
		method = getattr(export, method_name)
		try:
			method(**options)
		except Exception as e:
			print(e)
			print(str(e))
			return self.send_error(status_code=500)

		return self.write(dict(
			filename=export_file,
		))
