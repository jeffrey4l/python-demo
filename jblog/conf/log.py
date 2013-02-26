#!/usr/bin/env python
#-*- coding:utf-8 -*-
#Author: Lei Zhang <zhang.lei.fly@gmail.com>

import logging
import logging.config

CONF_MAPPING={
        'dev':'logging-dev.conf',
        'live':'logging-live.conf'
        }
logging.config.fileConfig

INITED=False

def get_logger(name, mode=None):
    global INITED
    if not INITED:
        logging.config.fileConfig(


