'''
Created on Apr 4, 2018

@author: smckinn
@copyright: 2018 - Symas Corporation
'''
from setuptools import setup

setup(name='py-fortress',
      version='0.1',
      description='Role-Based Access Control API for Python',
      url='https://github.com/shawnmckinney/py-fortress',
      author='Symas Corporation',
      author_email='support@symas.com',
      license='Apache 2.0',
      packages=['py-fortress'],
      install_requires=[
          'ldap3',
      ],      
      zip_safe=False)