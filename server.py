#!/usr/bin/env python3
from tornado.web import Application
from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop
from asyserver import AsyRunHandler
from argparse import ArgumentParser
from utils import print_stderr, drop_root_perm
import os

BASE_PORT=10007
TIMEOUT=60


def parse_args():
    parser = ArgumentParser()
    parser.add_argument('--port', type=int, default=BASE_PORT,
        help='Port to listen. Defaults to {0}'.format(BASE_PORT))
    parser.add_argument('--timeout', type=int, default=TIMEOUT,
        help='Timeout for asymptote, in seconds. Defaults to {0}'.format(
        TIMEOUT))
    return parser.parse_args()


def main():
    args = parse_args()
    main_application = Application([
        (r'/', AsyRunHandler, {'timeout': args.timeout})
        ])
    main_server = HTTPServer(main_application)
    # Drop any root permissions
    main_server.bind(args.port)

    try:
        if 'ASYMPTOTE_USER' in os.environ:
            username=os.environ['ASYMPTOTE_USER']
        else:
            username='asymptote'

        if 'ASYMPTOTE_GROUP' in os.environ:
            group=os.environ['ASYMPTOTE_GROUP']
        else:
            group='asymptote'

        drop_root_perm(username,group)
    except RuntimeError as e:
        print_stderr('DropPerm Msg: {0}', e)

    main_server.start()
    IOLoop.current().start()


if __name__ == '__main__':
    main()
