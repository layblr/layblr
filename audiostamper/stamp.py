import os

import tornado.ioloop

from audiostamper.server.app import create_app

if __name__ == '__main__':
	# Get the current directory and make it the root dir.
	root_dir = os.path.abspath(os.curdir)

	# Start app on localhost:8989
	app = create_app(root_dir, '0.0.0.0', 8989)
	print('Listening on: http://localhost:8989/')

	# Run forever.
	try:
		tornado.ioloop.IOLoop.current().start()
	except KeyboardInterrupt:
		print('Shutting down API server...')
