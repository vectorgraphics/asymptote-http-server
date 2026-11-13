#!/usr/bin/env python3
from tornado.web import RequestHandler

import subprocess as sp
import tempfile as tf
import io

# Appended after any client-supplied options, so a client can never
# override them: asy honors the last occurrence of each option.
SAFE_OPTS = ('-safe', '-noglobalread', '-noglobalwrite',
             '-nocurlAfterRead', '-q', '-noV')


class AsyRunHandler(RequestHandler):
    def initialize(self, timeout):
        self.timeout = timeout

    def get(self):
        outval = sp.run(['asy', '-version'], stdout=sp.PIPE, stderr=sp.PIPE)
        self.write(outval.stderr.decode('utf-8').replace('\n','<br>'))

    def post(self):
        fmt = 'html'
        args = ['asy']
        for opt, vals in self.request.query_arguments.items():
            val = vals[-1].decode('utf-8')
            if opt in ('f', 'outformat'):
                fmt = val
            else:
                args.append('-' + opt)
                if val:
                    args.append(val)
        with tf.TemporaryDirectory() as tfd:
            args += ['-f', fmt, '-o', tfd + '/out']
            args += SAFE_OPTS
            args.append('-')
            success=True
            proc=None
            try:
                proc = sp.run(
                    args, input=self.request.body,
                    timeout=self.timeout, stderr=sp.PIPE, stdout=sp.PIPE,
                    cwd=tfd)
            except sp.TimeoutExpired:
                success = False
                self.set_status(408)
                self.finish({'msg': 'Asymptote timeout'})

            if success:
                try:
                    proc.check_returncode()
                    with io.open(tfd + '/out.' + fmt, 'rb') as iof:
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
