#!/usr/bin/env python
# coding: utf-8
from setuptools import setup

with open("README.md", "r", encoding="utf-8") as fd:
    long_description = fd.read()

setup(
    name = 'ChatRoom-jianjun',
    version = '2.1.19',
    author = 'jianjun',
    author_email = '910667956@qq.com',
    url = 'https://github.com/EVA-JianJun/ChatRoom',
    description = u'Python分布式交互框架！快速建立可靠的网络连接！',
    long_description = long_description,
    long_description_content_type = "text/markdown",
    packages = ["ChatRoom"],
    install_requires = [
        "cprint-jianjun>=1.1.0",
        "pycryptodome>=3.15.0",
        "bcrypt>=3.2.0",
        "psutil>=5.7.0",
        "tqdm>=4.44.1",
        "Mconfig>=1.1.4",
        "ttkbootstrap>=1.9.0",
        "yagmail>=0.15.280",
        "pyperclip>=1.8.2",
    ],
    entry_points={
        'console_scripts': [
            'room=ChatRoom.gui:RunRoom'
        ],
    },
    package_data={
    '': ['config/*', '.Room/audio/*', '.Room/image/*', '.Room/image/anya/*'],
    },
)