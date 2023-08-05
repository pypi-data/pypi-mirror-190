# -*- coding: utf-8 -*-
# @Time : 2023/2/3 17:33
# @Author : Zdh
from setuptools import find_packages, setup
import os

VERSION = '0.0.6'

# readme文件
readme_file = os.path.join(os.path.dirname(__file__), 'README.md')
with open(readme_file, 'r', encoding='utf-8') as fp:
    long_description = fp.read()
#

setup(
    name='SimpleDLCV',
    version=VERSION,
    author='zdh',
    author_email='zhoudonghui0124@163.com',
    description='',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://gitee.com/small_eyes_zdh/SimpleDL',
    keywords='pytorch dl cv',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "tqdm>=4.64.1",
        "pyyaml==6.0",
    ],

    python_requires='>=3.8',
    classifiers=[
        'Operating System :: OS Independent',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.8',
    ],
)
