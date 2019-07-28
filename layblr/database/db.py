import asyncio

import aiosqlite

from layblr.database.repo import Repository
from layblr.database.schema import Schema


class Database:
	def __init__(self, database_file):
		self.file = database_file
		self.connection = None
		self.schema = Schema(self)
		self.repos = dict()

	async def connect(self):
		self.connection = await aiosqlite.connect(self.file)
		await self.schema.load_state()
		await self.schema.migrate()
		await self.connection.commit()

	def get_repository(self, model_class):
		"""
		Get repository for given model class.
		:param model_class: Model class (module).
		:return: Repository instance
		:rtype: layblr.database.repo.Repository
		"""
		if model_class not in self.repos:
			self.repos[model_class] = Repository(self, model_class)
		return self.repos[model_class]

	def get_repo(self, model_class):
		"""
		Get repository for given model class.
		:param model_class: Model class (module).
		:return: Repository instance
		:rtype: layblr.database.repo.Repository
		"""
		return self.get_repository(model_class)
