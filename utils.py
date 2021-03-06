#!/usr/bin/env python3
import sys
import os, pwd, grp, getpass

def print_stderr(msg: str, *args):
    sys.stderr.write(msg.format(args))
    sys.stderr.write('\n')
    sys.stderr.flush()


def drop_root_perm(username, group, umask=0o077):
    if sys.platform.startswith('win32'):
        raise RuntimeError('Cannot run on Windows platforms')
    if getpass.getuser() != 'root':
        return

    try:
        newUid = pwd.getpwnam(username).pw_uid
        newGid = grp.getgrnam(group).gr_gid
    except KeyError:
        raise RuntimeError('Username or Group not found')

    os.setgroups([])
    os.setgid(newGid)
    os.setuid(newUid)

    os.environ['HOME']=os.path.expanduser('~'+username)
    print_stderr('Root permissions dropped')
    return os.umask(umask)
