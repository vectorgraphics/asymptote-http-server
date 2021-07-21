#!/usr/bin/env python3
from asyopts import AsymptoteOpts
from tornado.web import RequestHandler

import subprocess as sp
import tempfile as tf
import os, io

class AsyRunHandler(RequestHandler):
    def initialize(self, timeout):
        self.asyopt = AsymptoteOpts()
        self.timeout = timeout

    def prepare(self):
        for opt, val in self.request.query_arguments.items():
            val_decoded = val[-1].decode('utf-8')
            if opt == 'flag':
                self.asyopt.setOpt(val_decoded)
            else:
                self.asyopt.setOpt(opt, val_decoded)
        if self.asyopt.mimeType():
            self.set_header(
                'Content-Type', self.asyopt.mimeType() + '; charset=UTF-8')

    def get(self):
        outval = sp.run(['asy', '-version'], stdout=sp.PIPE, stderr=sp.PIPE)
        self.write(outval.stderr.decode('utf-8'))

    def post(self):
        with tf.TemporaryDirectory() as tfd:
            self.asyopt.tmpDir=tfd
            # print(self.asyopt.createArgs())
            success=True
            proc=None
            try:
                proc = sp.run(
                    self.asyopt.createArgs(), input=self.request.body,
                    timeout=self.timeout, stderr=sp.PIPE)
            except TimeoutError:
                success = False
                self.set_status(408)
                self.finish({'msg': 'Asymptote timeout'})

            if success:
                try:
                    with io.open(self.asyopt.getFilePath(), 'rb') as iof:
                        self.set_status(200)
                        self.write(iof.read())
                except FileNotFoundError:
                    self.set_status(415)
                    self.finish({
                        'msg': 'Asymptote error',
                        'reason': proc.stderr.decode('utf-8').strip()
                        })
        self.flush()
