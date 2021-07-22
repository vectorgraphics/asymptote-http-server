#!/usr/bin/env python3
from tornado.web import Application
from tornado.ioloop import IOLoop
from asyserver import AsyRunHandler
from argparse import ArgumentParser
from pwd import getpwnam
from os import setgid,setuid

BASE_PORT=10007
TIMEOUT=60

def parse_args():
    parser = ArgumentParser()
    parser.add_argument('--port', type=int, default=BASE_PORT,
        help='Port to listen. Defaults to {0}'.format(BASE_PORT))
    parser.add_argument('--timeout', type=int, default=TIMEOUT,
        help='Timeout for asymptote, in seconds. Defaults to {0}'.format(TIMEOUT))
    return parser.parse_args()


def main():
    args = parse_args()
    main_listener = Application([(r'/', AsyRunHandler, {'timeout': args.timeout})])
    main_listener.listen(args.port)
    # Drop any root permissions
    pwnam=getpwnam('asymptote')
    gid=pwnam.pw_gid
    uid=pwnam.pw_uid
    setgid(gid);
    setuid(uid);
    IOLoop.current().start()


if __name__ == '__main__':
    main()
