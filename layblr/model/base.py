from layblr.database.exception import NotInjected


class BaseModel:
	"""
	Base model.

	:type _storage: node.storage.storage.StorageManager
	:type _repository: node.storage.repo.Repository
	:type _dirty: bool
	"""
	TABLE_NAME = None
	ID_COLUMN = 'id'

	def __init__(self, *args, **kwargs):
		self._storage = None
		self._repository = None
		self._dirty = True

		for key, value in kwargs.items():
			if not key.startswith('_'):
				self.__setattr__(key, value)

	def load(self, row):
		self._dirty = False
		# Implement in model!

	def to_row(self):
		raise NotImplementedError

	def to_json(self):
		return dict()

	def inject(self, repository):
		self._repository = repository
		self._storage = repository.storage_manager

	def _fetch_relation(self, model, **clause):
		if not self._storage:
			raise NotInjected()

		repo = self._repository.storage_manager.get_repository(model)
		return repo.get_one_by(clause)
