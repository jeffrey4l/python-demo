#!/usr/bin/env python
#-*- coding:utf-8 -*-
from setuptools import setup, find_packages

setup(
        name='jblog',
        version='1.0',
        url='http://www.infohold.com.cn',
        description="this is my blog program",
        author="Jeffrey4l",
        author_email="zhang.lei.fly@gmail.com",
        packages=find_packages(),
        install_requires=['bottle'],
        )

