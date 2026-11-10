
#!/usr/bin/env python3
# Options a client may never set or unset: the server decides these.
ASY_LOCKED_OPTS = {'safe', 'globalread', 'globalwrite', 'o', 'outname'}

# Forced on every request, before any client-supplied options.
ASY_SAFE_OPTS = ('-safe', '-noglobalread', '-noglobalwrite', '-q', '-noV')


class AsymptoteOpts:
    def __init__(self, fmt='html'):
        self.fmt = fmt
        self.tmpDir = None
        self.user_opts = []

    def isLocked(self, opt: str) -> bool:
        if opt.startswith('no'):
            return opt in ASY_LOCKED_OPTS or opt[2:] in ASY_LOCKED_OPTS
        return opt in ASY_LOCKED_OPTS

    def setOpt(self, opt, val=None):
        if self.isLocked(opt):
            return
        if opt in ('f', 'outformat'):
            self.fmt = val
        else:
            self.user_opts.append('-' + opt)
            if val:
                self.user_opts.append(val)

    def createArgs(self):
        return (['asy'] + list(ASY_SAFE_OPTS) + self.user_opts
                + ['-f', self.fmt, '-o', self.tmpDir + '/out', '-'])

    def getFilePath(self):
        if self.tmpDir:
            return self.tmpDir + '/out.' + self.fmt
        return None

