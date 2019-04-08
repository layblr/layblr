import os
import tornado.ioloop

from audiostamper.server.app import create_app


def execute_from_cli():
	# Get the current directory and make it the root dir.
	root_dir = os.path.abspath(os.curdir)

	# Start app on localhost:8989
	hostname = '0.0.0.0'
	port = 8989
	app = create_app(root_dir, hostname, port)
	print('Listening on: http://{}:{}/'.format(hostname, port))

	# Run forever.
	try:
		tornado.ioloop.IOLoop.current().start()
	except KeyboardInterrupt:
		print('Shutting down API server...')


if __name__ == '__main__':
	execute_from_cli()
