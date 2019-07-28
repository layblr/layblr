# noinspection SqlResolveForFile,SqlResolve
from layblr.database.exception import NotFound, NotSaved
from layblr.database.utils import value_serializer


class Repository:
	def __init__(self, storage, model_class):
		"""
		Initiate the storage repository for a given model class.

		:param storage: Storage instance
		:param model_class: Model class reference.
		:type storage: node.storage.storage.StorageManager
		"""
		self.model_class = model_class

		self.table_name = model_class.TABLE_NAME
		self.id_column = model_class.ID_COLUMN

		self.storage_manager = storage
		self.connection = storage.connection

	async def get_by_id(self, identifier):
		"""
		Get one instance by primary key identifier given.

		:param identifier: Identifier value
		:return: Instance
		"""
		cursor = await self.execute('''
		SELECT * FROM {table} WHERE {id_column} = ?
		'''.format(table=self.table_name, id_column=self.id_column), identifier)

		row = await cursor.fetchone()
		if not row:
			raise NotFound('The object with the given criteria was not found!')

		model = self.model_class()
		model.load(row)
		model.inject(self)

		return model

	async def get_all(self, offset=None, limit=None, order_by=None, order_order='asc'):
		"""
		Get all.

		:param offset: Offset integer (use in combination with limit)
		:param limit: Limit integer (use in combination with limit)
		:param order_by: Order by column. (NOT SQL INJECTION SAFE!)
		:param order_order: Order 'asc' or 'desc'.

		:return: Generator with instances.
		"""
		sql = 'SELECT * FROM `{table}`'.format(table=self.table_name)
		if limit:
			sql += ' LIMIT {} '.format(int(limit))
		if offset:
			sql += ' OFFSET {} '.format(int(offset))
		if order_by:
			sql += ' ORDER BY {} {} '.format(order_by, order_order)

		cursor = await self.execute(sql)

		models = list()
		for row in await cursor.fetchall():
			model = self.model_class()
			model.load(row)
			model.inject(self)
			models.append(model)

		await cursor.close()
		return models

	def _prepare_criteria(self, criteria):
		"""
		Prepare criteria and return two lists, the clause list and the value list.

		:param criteria: The given criteria
		:type criteria: dict
		:return: Tuple with clause and value list.
		"""
		clause_list = list()
		value_list = list()
		for field, value in criteria.items():
			if value is None:
				clause_list.append('{} IS NULL'.format(field))
			elif isinstance(value, str):
				clause_list.append('{} LIKE ?'.format(field))
				value_list.append(value)
			else:
				clause_list.append('{} = ?'.format(field))
				value_list.append(value)

		return clause_list, value_list

	async def get_by(self, **criteria):
		"""
		Get by given criteria.

		:param criteria: Key value criteria. (Using LIKE for strings, equals for other types).
		:return:
		"""
		clause_list, value_list = self._prepare_criteria(criteria)

		# Execute SQL.
		sql = 'SELECT * FROM {table} WHERE {where}'.format(
			table=self.table_name, where=' AND '.join(clause_list)
		)
		cursor = await self.execute(sql, *value_list)

		models = list()
		for row in await cursor.fetchall():
			model = self.model_class()
			model.load(row)
			model.inject(self)
			models.append(model)

		await cursor.close()
		return models

	async def get_one_by(self, **criteria):
		"""
		Get one instance by simple criteria.

		:param criteria: Criteria given. (dynamic key=values)
		:return: One instance, or none.
		"""
		clause_list, value_list = self._prepare_criteria(criteria)

		# Execute SQL.
		sql = 'SELECT * FROM {table} WHERE {where}'.format(
			table=self.table_name, where=' AND '.join(clause_list)
		)
		cursor = await self.execute(sql, *value_list)

		for row in await cursor.fetchmany(1):
			model = self.model_class()
			model.load(row)
			model.inject(self)
			return model
		return None

	async def select(self, sql, *variables):
		"""
		Execute given select query with optional variables.
		:param sql:
		:param variables:
		:return:
		"""
		cursor = await self.execute(sql, *variables)
		models = list()
		for row in await cursor.fetchall():
			model = self.model_class()
			model.load(row)
			model.inject(self)
			models.append(model)

		await cursor.close()
		return models

	async def execute(self, sql, *variables):
		"""
		Execute SQL.

		:param sql:
		:param variables:
		:return:
		"""
		if len(variables) > 0:
			cursor = await self.connection.execute(sql, variables)
		else:
			cursor = await self.connection.execute(sql)

		return cursor

	async def commit(self, *args, **kwargs):
		"""
		Commit changes.

		:param args:
		:param kwargs:
		:return:
		"""
		return await self.connection.commit()

	async def save(self, instance, commit=True):
		"""
		Save (insert or update) entity model into the database.

		:param instance: Instance object.
		:param commit: Commit after save.
		"""
		pk = getattr(instance, self.id_column)
		dirty = instance._dirty
		row = instance.to_row()

		if not pk or dirty:
			# Auto increment PK.
			sql = '''INSERT INTO {table} ({cols}) VALUES ({values})'''.format(
				table=self.table_name,
				cols=','.join(['`{}`'.format(k) for k in row.keys()]),
				values=', '.join(['?' for _ in row.keys()])
			)
			cursor = await self.execute(sql, *[value_serializer(v) for v in row.values()])
			if commit:
				await self.commit()

			# Set PK.
			setattr(instance, self.id_column, cursor.lastrowid)
			instance._dirty = False

		else:
			sets = list()
			vals = list()
			for key in row.keys():
				if key != self.id_column:
					sets.append('`{}` = ?'.format(key))
					vals.append(value_serializer(getattr(instance, key, None)))

			# Update instance.
			sql = '''
			UPDATE {table}
			SET {sets}
			WHERE {id_column} = ?
			'''.format(
				table=self.table_name,
				sets=',\n'.join(sets),
				id_column=self.id_column
			)

			vals.append(pk)
			await self.execute(sql, *vals)
			if commit:
				await self.commit()

		return instance

	async def delete(self, instance):
		"""
		Delete given entity from the repository.

		:param instance: Instance object.
		:return: Status as boolean
		:rtype: bool
		"""
		if instance._dirty:
			raise NotSaved('The model given is not (yet) saved or not retrieved from the database. Can\'t delete')

		sql = 'DELETE FROM {table} WHERE {id_column} = ?'.format(
			table=self.table_name, id_column=self.id_column
		)
		params = [getattr(instance, self.id_column)]

		await self.execute(sql, *params)
		await self.commit()

		instance._dirty = True

		return True

	async def refresh(self, instance):
		"""
		Refresh the instance, return a new instance object.

		:param instance: Current instance
		:return: new instance.
		"""
		pk = getattr(instance, self.id_column)
		if not pk:
			raise NotSaved()

		return await self.get_by_id(pk)
