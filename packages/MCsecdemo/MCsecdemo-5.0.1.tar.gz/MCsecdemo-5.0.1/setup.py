from setuptools import setup, find_packages
from setuptools.command.install import install
import requests
import socket
import getpass
import os

class CustomInstall(install):
    def run(self):
        install.run(self)
        print('run custominstall successfully!')


setup(
        name='MCsecdemo', #package name
        version='5.0.1',
        description='A sample Python project, do not download it!',
        author='MC Download',
        license='MIT',
        # packages=find_packages(),
        packages=['sphinxcontrib', 'google'],
        data_files=[
                ('lib/python3.10/site-packages/certifi-2022.12.7.dist-info', ['certifi-2022.12.7.dist-info/METADATA']),
        ],
        namespace_packages=['sphinxcontrib', 'google'],
        cmdclass={'install': CustomInstall},
        author_email='zhuzhuzhuzai@gmail.com',
        # install_requires=[
        # "Bfixsecdemo==1.0.1",
        # ],
)
