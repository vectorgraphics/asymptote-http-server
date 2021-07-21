#!/usr/bin/env python3
import mimetypes

ASY_LOCKED_OPTS = {
    'safe', 'globalread', 'globalwrite', 'o', 'outname'
    }

class AsymptoteOpts:
    def __init__(self, fmt='png'):
        self.base_opts = {
            'globalread': False,
            'globalwrite': False,
            'safe': None,
            'q': None,
            'noV': None
        }
        self.tmpDir = None
        self.fmt = fmt
        self.locked_opts = set(ASY_LOCKED_OPTS)

    def isLocked(self, arg: str) -> bool:
        isLock = arg in self.locked_opts
        if arg.startswith('no'):
            isNoLock = arg[2:] in self.locked_opts
            return isLock or isNoLock
        else:
            return isLock

    def mimeType(self):
        return mimetypes.guess_extension(self.fmt)

    def setOpt(self, opt, val=None):
        if not self.isLocked(opt):
            if opt == 'f':
                self.fmt = val
            else:
                if val == False and not opt.startswith('no'):
                    self.base_opts['no'+opt] = None
                else:
                    self.base_opts[opt] = val

    def delOpt(self, opt: str):
        if not self.isLocked(opt) and opt in self.base_opts:
            self.base_opts.pop(opt)
        if opt.startswith('no'):
            rawopt = opt[2:]
            if rawopt in self.base_opts:
                self.base_opts.pop(rawopt)

    def createArgs(self):
        base_args = ['asy']
        for opt, val in self.base_opts.items():
            base_args.append('-'+opt)
            if val:
                base_args.append(val)
        base_args.append('-f'+self.fmt)
        base_args.append('-o'+self.tmpDir+'/out')
        base_args.append('-')
        return base_args

    def getFilePath(self):
        if self.tmpDir:
            return self.tmpDir + '/out.' + self.fmt
        else:
            return None
