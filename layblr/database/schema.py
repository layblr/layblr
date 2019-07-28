import logging

from layblr.database.migrator import get_migration_versions, get_latest_version, get_version_class

logger = logging.getLogger(__name__)


class Schema:
	def __init__(self, storage):
		"""
		Initiate schema manager
		:param storage: Storage manager instance.
		:type storage: layblr.database.db.Database
		"""
		self.storage = storage
		self.current_version = 0
		self.versions = get_migration_versions()
		self.latest_version = get_latest_version()
		self.versions_todo = list()

	async def check_schema_table(self):
		try:
			await self.storage.connection.execute('SELECT 1 FROM schema_version;')
		except:
			print('Please ignore the error about the missing table')
			await self.storage.connection.executescript(
				'''
				CREATE TABLE schema_version (
					version		INT 	NOT NULL	PRIMARY KEY,
					applied_at	DATE	NOT NULL
				);
				''')
			await self.storage.connection.executescript(
				'''
				INSERT INTO schema_version VALUES (0, CURRENT_DATE)
				'''
			)
		await self.storage.connection.commit()

	async def load_state(self):
		"""
		Load current database version state.
		"""
		# Check and create schema version table.
		await self.check_schema_table()

		# Get current version history.
		cursor = await self.storage.connection.execute('SELECT * FROM schema_version ORDER BY version DESC LIMIT 1')
		self.current_version = (await cursor.fetchone())[0]

		self.versions_todo = list(range(self.current_version + 1, self.latest_version + 1))

	async def migrate(self):
		"""
		Execute all the migrations that are ready to execute.

		:return:
		"""
		for version_number in self.versions_todo:
			clazz = get_version_class(version_number)
			migrator = clazz(self.storage)

			# Try to migrate up.
			print('Migrating database... Executing migration {}'.format(version_number))
			await migrator.up()

			# Insert version into db.
			await self.storage.connection.execute('INSERT INTO schema_version VALUES (?, CURRENT_DATE)', [
				version_number
			])
			await self.storage.connection.commit()

		# Update the current version variable + log the migration results.
		if len(self.versions_todo) > 0:
			print('Completed {} migration(s)'.format(len(self.versions_todo)))
			logger.info('Completed {} migration(s)'.format(len(self.versions_todo)))

			self.versions_todo = list()
			self.current_version = self.latest_version
