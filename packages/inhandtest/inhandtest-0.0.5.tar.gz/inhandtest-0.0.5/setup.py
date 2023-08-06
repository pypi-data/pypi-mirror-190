# -*- coding: utf-8 -*-
# @Time    : 2023/1/31 16:47:12
# @Author  : Pane Li
# @File    : setup.py
"""

setup

"""
from distutils.core import setup

setup(
    name='inhandtest',
    version='0.0.5',
    author='liwei',
    author_email='liwei@inhand.com.cn',
    description='inhand test tools, so easy',
    maintainer='liwei',
    maintainer_email='liwei@inhand.com.cn',
    py_modules=['inhandtest.tools', 'inhandtest.telnet'],
    long_description='inhand test tools, so easy',
    classifiers=[
        "Programming Language :: Python :: 3.7",
    ],
    install_requires=[  # 这里是依赖列表，表示运行这个包的运行某些功能还需要你安装其他的包
    ]
)
