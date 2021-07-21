#!/usr/bin/env python3
from tornado.web import Application
from tornado.ioloop import IOLoop

from asyrunner import AsyRunHandler

BASE_PORT=10007
TIMEOUT=60

def main():
    main_listener = Application([(r'/', AsyRunHandler, {'timeout': TIMEOUT})])
    main_listener.listen(BASE_PORT)
    IOLoop.current().start()


if __name__ == '__main__':
    main()
