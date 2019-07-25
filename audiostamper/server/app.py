import os
import jinja2
import tornado.web

from tornado_jinja2 import Jinja2Loader
from tornado.log import enable_pretty_logging
from tornado.web import StaticFileHandler, RedirectHandler

from audiostamper.handler.analyse import AnalyseHandler
from audiostamper.handler.browser import BrowserHandler
from audiostamper.handler.export import ExportHandler
from audiostamper.handler.importer import ImporterHandler
from audiostamper.handler.audio import AudioFileHandler
from audiostamper.handler.spa import AppHandler


class App(tornado.web.Application):
	def __init__(self, root_dir, handlers=None, default_host=None, transforms=None, **settings):
		self.root_dir = root_dir
		self.build_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'dist', 'stamper')

		if not handlers:
			handlers = list()

		handlers += [
			(r'/', 									RedirectHandler, dict(url='/index.html')),
			(r'/ajax/browse', 						BrowserHandler),
			(r'/ajax/export', 						ExportHandler),
			(r'/ajax/import', 						ImporterHandler),
			(r'/ajax/analyse/(?P<file>[^\/]+)',		AnalyseHandler),
			(r'/ajax/audio/(.+\.(mp3|wav))', 		StaticFileHandler, dict(path=self.root_dir)),
			# (r'/ajax/audio/(.+\.(mp3|wav))',		AudioFileHandler),
			(r'/(.*)',								AppHandler, dict(path=self.build_dir)),
		]

		enable_pretty_logging()
		settings['template_path'] = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'template')
		settings['debug'] = True
		settings['autoreload'] = False

		jinja2_env = jinja2.Environment(
			loader=jinja2.FileSystemLoader(settings['template_path']),
			autoescape=True
		)
		jinja2_loader = Jinja2Loader(jinja2_env)
		settings['template_loader'] = jinja2_loader

		settings['default_handler_class'] = AppHandler

		super().__init__(handlers, default_host, transforms, **settings)


def create_app(root_dir, listen_address, listen_port):
	app = App(root_dir)
	app.listen(listen_port, listen_address)
	return app
