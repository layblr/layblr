import asyncio
import os
import signal

import tornado.ioloop
from tornado.platform.asyncio import AsyncIOMainLoop

from layblr.server.app import create_app

signal_received = False


def execute_from_cli():
	# Get the current directory and make it the root dir.
	root_dir = os.path.abspath(os.curdir)

	# Preparations
	AsyncIOMainLoop().install()
	loop = asyncio.get_event_loop()

	# Prepare the app.
	hostname = '0.0.0.0'
	port = 8989
	app = loop.run_until_complete(create_app(root_dir))

	signal.signal(signal.SIGINT, signal.SIG_DFL)

	# Start the server.
	app.listen(port, hostname)
	print('Listening on: http://{}:{}/'.format(hostname, port))
	try:
		loop.run_forever()
	except KeyboardInterrupt:
		pass


if __name__ == '__main__':
	execute_from_cli()
