import asyncio
import os
import jinja2
import tornado.web

from tornado_jinja2 import Jinja2Loader
from tornado.log import enable_pretty_logging
from tornado.web import StaticFileHandler, RedirectHandler

from layblr.database.db import Database
from layblr.handler.analyse import AnalyseHandler
from layblr.handler.api.browser import ProjectBrowseHandler
from layblr.handler.api.project import ProjectHandler, ProjectDetailHandler
from layblr.handler.browser import BrowserHandler
from layblr.handler.export import ExportHandler
from layblr.handler.importer import ImporterHandler
from layblr.handler.audio import AudioFileHandler
from layblr.handler.spa import AppHandler


class App(tornado.web.Application):
	def __init__(self, root_dir, db, handlers=None, default_host=None, transforms=None, **settings):
		self.root_dir = root_dir
		self.data_dir = os.path.join(root_dir, 'data')
		if not os.path.exists(self.data_dir):
			os.mkdir(self.data_dir)

		self.db = db
		self.build_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'dist', 'layblr')

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

			(r'/api/project',												ProjectHandler),
			(r'/api/project/(?P<project_id>[0-9]+)',						ProjectDetailHandler),
			(r'/api/project/(?P<project_id>[0-9]+)/browse',					ProjectBrowseHandler),
			(r'/api/project/(?P<project_id>[0-9]+)/browse/(?P<path>.*)',	ProjectBrowseHandler),

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


async def create_app(root_dir):
	db = Database(os.path.join(root_dir, 'database.sqlite3'))
	await db.connect()

	app = App(root_dir, db)
	return app
