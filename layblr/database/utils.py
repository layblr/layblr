import datetime
import json


def value_serializer(value):
	if value is None:
		return None
	if isinstance(value, dict):
		return json.dumps(value)
	if isinstance(value, (list, tuple)):
		return json.dumps(value)
	if isinstance(value, datetime.datetime):
		return value.strftime('%Y-%m-%d %H:%M:%S')
	if isinstance(value, datetime.date):
		return value.strftime('%Y-%m-%d %H:%M:%S')
	if isinstance(value, (int, float)):
		return value
	return str(value)


def parse_datetime(value) -> datetime.datetime:
	return datetime.datetime.strptime(value, '%Y-%m-%d %H:%M:%S')


def format_datetime(dt: datetime.datetime) -> str:
	return dt.strftime('%Y-%m-%d %H:%M:%S')
