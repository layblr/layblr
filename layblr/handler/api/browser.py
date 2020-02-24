import json
import os

import tornado.web
from jinja2.filters import do_filesizeformat

from layblr.database.repo import Repository
from layblr.model.project import Project


class ProjectBrowseHandler(tornado.web.RequestHandler):
	SUPPORTED_METHODS = tornado.web.RequestHandler.SUPPORTED_METHODS

	def __init__(self, *args, **kwargs):
		self.project_repo = None  # type: Repository
		self.project = None  # type: Project
		self.base = ''
		self.path = ''
		super().__init__(*args, **kwargs)

	async def prepare(self):
		self.project_repo = self.application.db.get_repo(Project)
		self.project = await self.project_repo.get_by_id(self.path_kwargs['project_id'])
		self.base = self.project.directory
		if 'path' in self.path_kwargs:
			self.path = self.path_kwargs['path']

	async def get(self, *args, **kwargs):
		path = os.path.abspath(os.path.join(self.base, self.path))
		if not path.startswith(self.base):
			self.set_status(403)
			await self.finish(dict(error='Directory not inside project directory'))
			return
		if not os.path.exists(path):
			self.set_status(404)
			await self.finish(dict(error='File or directory not found!'))
			return

		# If directory, return the directory structure inside.
		if os.path.isdir(path):
			listing = list()

			for item in os.listdir(path):
				full_path = os.path.join(path, item)
				is_dir = os.path.isdir(full_path)
				size = 0
				if not is_dir:
					size = os.path.getsize(full_path)
				modified_time = os.path.getmtime(full_path)
				create_time = os.path.getctime(full_path)

				listing.append(dict(
					item=item,
					is_dir=is_dir,
					path=full_path,
					directory=path,
					size=size,
					modified_time=modified_time,
					create_time=create_time
				))

			listing = sorted(listing, key=lambda k: k['is_dir'], reverse=True)

			self.write(dict(
				data=dict(
					directory=path,
					base_directory=self.base,
					listing=listing,
				)
			))
			return
		else:
			# TODO: Download file.
			pass

		self.write(dict())

	async def post(self, *args, **kwargs):
		pass

	async def delete(self, *args, **kwargs):
		pass

	async def put(self, *args, **kwargs):
		pass
