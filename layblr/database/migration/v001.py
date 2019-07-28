from layblr.database.migrator import Migrator


class Version001(Migrator):
	async def up(self):
		# Create tables.
		########################################################################
		await self.connection.executescript("""
		CREATE TABLE project
		(
			id INTEGER PRIMARY KEY AUTOINCREMENT,
			name TEXT NOT NULL,
			directory TEXT,
			created_at DATETIME NOT NULL DEFAULT (datetime('now','localtime'))
		);
		""")
