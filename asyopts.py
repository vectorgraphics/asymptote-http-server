#!/usr/bin/env python3
import mimetypes

ASY_LOCKED_OPTS = {
    'safe', 'globalread', 'globalwrite', 'o', 'outname'
    }

class AsymptoteOpts:
    def __init__(self, fmt='html'):
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
            if opt == 'f' or opt == 'outformat':
                self.fmt = val
            else:
                if val == False and not opt.startswith('no'):
                    self.base_opts['no'+opt] = None
                else:
                    self.base_opts[opt] = val

    def createArgs(self):
        base_args = ['asy']
        for opt, val in self.base_opts.items():
            base_args.append('-'+opt)
            if val:
                base_args.append(val)
        base_args.extend(['-f',self.fmt,'-o',self.tmpDir+'/out','-'])
        return base_args

    def getFilePath(self):
        if self.tmpDir:
            return self.tmpDir + '/out.' + self.fmt
        else:
            return None
