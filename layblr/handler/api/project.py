import json

import tornado.web
from jinja2.filters import do_filesizeformat

from layblr.database.repo import Repository
from layblr.model.project import Project


class ProjectHandler(tornado.web.RequestHandler):
	SUPPORTED_METHODS = tornado.web.RequestHandler.SUPPORTED_METHODS

	def __init__(self, *args, **kwargs):
		self.repo = None  # type: Repository
		super().__init__(*args, **kwargs)

	async def prepare(self):
		self.repo = self.application.db.get_repo(Project)

	async def get(self, *args, **kwargs):
		projects = await self.repo.get_all()
		self.write(dict(data=[e.to_json() for e in projects]))

	async def post(self, *args, **kwargs):
		raw = json.loads(self.request.body.decode())
		if 'name' not in raw:
			self.set_status(400)
			await self.finish(dict(error='Invalid arguments'))
			return

		entity = Project()
		entity.name = raw['name']

		# TODO: Make this safe, use authentication or setting to allow this.
		if 'directory' in raw:
			entity.directory = raw['directory']

		await self.repo.save(entity)
		entity.create_folder(self.application.data_dir)
		await self.repo.save(entity)

		self.write(dict(data=entity.to_json()))


class ProjectDetailHandler(tornado.web.RequestHandler):
	SUPPORTED_METHODS = tornado.web.RequestHandler.SUPPORTED_METHODS

	def __init__(self, *args, **kwargs):
		self.repo = None  # type: Repository
		super().__init__(*args, **kwargs)

	async def prepare(self):
		self.repo = self.application.db.get_repo(Project)

	async def get(self, project_id, *args, **kwargs):
		project = await self.repo.get_by_id(project_id)
		self.write(dict(data=project.to_json()))
