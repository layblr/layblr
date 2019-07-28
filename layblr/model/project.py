import os

from layblr.model.base import BaseModel


class Project(BaseModel):
	"""
	Project model.

	:type id: int
	:type name: str
	"""
	TABLE_NAME = 'project'

	# noinspection PyTypeChecker
	def __init__(self, *args, **kwargs):
		self.id = None
		self.name = None

		self.directory = None

		super().__init__(*args, **kwargs)

	def load(self, row):
		super().load(row)
		self.id, self.name, self.directory = row[:3]

	def to_row(self):
		return dict(
			id=self.id,
			name=self.name,
			directory=self.directory,
		)

	def to_json(self):
		return dict(
			id=self.id,
			name=self.name,
			directory=self.directory,
		)

	def create_folder(self, data_dir):
		self.directory = os.path.join(data_dir, 'pr_{}'.format(self.id))
		if not os.path.exists(self.directory):
			os.mkdir(self.directory)
		return self.directory
