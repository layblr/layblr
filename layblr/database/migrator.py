import importlib


class Migrator:
	VERSION = None

	def __init__(self, db):
		"""
		Initiate migrator class.

		:param db: Database instance
		:type db: layblr.database.db.Database
		"""
		self.db = db
		self.connection = db.connection

	async def up(self):
		"""
		Migrate the schema to the new version.
		"""
		raise NotImplementedError

	async def down(self):
		"""
		Migrate down to the older version (undo changes). Optional but recommended.
		:return:
		"""
		raise Exception('No down migration')


def get_migration_versions():
	"""
	Scan folder for migration versions and return the version classes.

	:return: Version migrator classses.
	"""
	from layblr.database.migration import versions
	return versions


def get_latest_version():
	"""
	Get latest version.

	:return: Latest version number
	"""
	versions = get_migration_versions()
	return int(versions[len(versions) - 1])


def get_version_class(version):
	"""
	Import and return class of the given integer version.
	:param version: Version integer.
	:return: Class of the migration version.
	"""
	version_string = '{0:03d}'.format(version)
	module_name = 'v{}'.format(version_string)
	version_class = 'Version{}'.format(version_string)

	module = importlib.import_module('layblr.database.migration.{}'.format(module_name))
	return getattr(module, version_class)
