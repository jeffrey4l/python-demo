#-*- coding:utf-8 -*-

import os

from cfg import get_cfg, Config

class ConfError(Exception):
    pass
        


def _get_mode(mode=None):
    env_mode = os.environ.get('MODE', None)
    real_mode = mode if mode else env_mode if env_mode else None
    if not real_mode:
        raise ConfError('the "MODE" must be specify explicit in the os env variable')
    return real_mode

MODE = _get_mode()

CFG=get_cfg(mode=MODE)

from default import *
if MODE == 'live':
    from live import *
elif MODE == 'dev':
    from dev import *
