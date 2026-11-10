#!/usr/bin/env python3
from asyopts import AsymptoteOpts
from tornado.web import RequestHandler

import subprocess as sp
import tempfile as tf
import io

class AsyRunHandler(RequestHandler):
    def initialize(self, timeout):
        self.asyopt = AsymptoteOpts()
        self.timeout = timeout

    def prepare(self):
        for opt, val in self.request.query_arguments.items():
            self.asyopt.setOpt(opt, val[-1].decode('utf-8'))

    def get(self):
        outval = sp.run(['asy', '-version'], stdout=sp.PIPE, stderr=sp.PIPE)
        self.write(outval.stderr.decode('utf-8').replace('\n','<br>'))

    def post(self):
        with tf.TemporaryDirectory() as tfd:
            self.asyopt.tmpDir=tfd
            success=True
            proc=None
            try:
                proc = sp.run(
                    self.asyopt.createArgs(), input=self.request.body,
                    timeout=self.timeout, stderr=sp.PIPE, stdout=sp.PIPE,
                    cwd=self.asyopt.tmpDir)
            except sp.TimeoutExpired:
                success = False
                self.set_status(408)
                self.finish({'msg': 'Asymptote timeout'})

            if success:
                try:
                    proc.check_returncode()
                    with io.open(self.asyopt.getFilePath(), 'rb') as iof:
                        self.set_status(200)
                        self.write(iof.read())
                except sp.CalledProcessError:
                    self.set_status(415)
                    self.finish({
                        'msg': 'Asymptote error.',
                        'reason': proc.stderr.decode('utf-8').strip()
                        })
                except FileNotFoundError:
                    self.set_status(204)
