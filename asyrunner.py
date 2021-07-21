#!/usr/bin/env python3
from asyopts import AsymptoteOpts
from tornado.web import RequestHandler

import subprocess as sp
import tempfile as tf
import os, io

class AsyRunHandler(RequestHandler):
    def initialize(self):
        self.asyopt = AsymptoteOpts()

    def prepare(self):
        for opt, val in self.request.query_arguments.items():
            val_decoded = val[-1].decode('utf-8')
            if opt == 'flag':
                self.asyopt.setOpt(val_decoded)
            else:
                self.asyopt.setOpt(opt, val_decoded)
        if self.asyopt.mimeType():
            self.set_header('Content-Type', self.asyopt.mimeType() + '; charset=UTF-8')

    def get(self):
        outval = sp.run(['asy', '-version'], stdout=sp.PIPE, stderr=sp.PIPE)
        self.write(outval.stderr.decode('utf-8'))

    def post(self):
        with tf.TemporaryDirectory() as tfd:
            self.asyopt.tmpDir=tfd
            print(self.asyopt.createArgs())
            sp.run(self.asyopt.createArgs(), input=self.request.body)
            try:
                with io.open(self.asyopt.getFilePath(), 'rb') as iof:
                    self.write(iof.read())
            except FileNotFoundError:
                self.write_error(415)
        self.flush()
