#!/usr/bin/env python3
from tornado.web import (
    Application,
    RequestHandler
)

from tornado.ioloop import IOLoop
import subprocess as sp
import tempfile as tf
import os, io


BASE_PORT=10007


class AsyRunHandler(RequestHandler):
    def initialize(self):
        pass

    async def prepare(self):
        pass

    def get(self):
        outval = sp.run(['asy', '-version'], stdout=sp.PIPE, stderr=sp.PIPE)
        self.write(outval.stderr.decode('utf-8'))

    def post(self):
        with tf.TemporaryDirectory() as tfd:
            outfile = '{0}/out.png'.format(tfd)
            sp.run(['asy', '-noV', '-o'+outfile, '-fpng', '--'],
                input=self.request.body)
            with io.open(outfile, 'rb') as iof:
                self.write(iof.read())


def main():
    main_listener = Application([(r'/upd', AsyRunHandler)])
    main_listener.listen(BASE_PORT)
    IOLoop.current().start()


if __name__ == '__main__':
    main()
