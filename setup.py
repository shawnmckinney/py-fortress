'''
Created on Apr 4, 2018

@author: smckinn
@copyright: 2018 - Symas Corporation
'''
from setuptools import setup
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(name='py-fortress',
      version='0.0.7',
      python_requires='>=3',
      description='RBAC for Python',
      long_description=long_description,
      long_description_content_type="text/markdown",
      url='https://github.com/shawnmckinney/py-fortress',
      author='Symas Corporation',
      author_email='smckinney@symas.com,ebackes@symas.com',
      license='Apache License 2.0',      
      packages=['pyfortress', 'pyfortress.doc', 'pyfortress.impl', 'pyfortress.ldap', 'pyfortress.model', 'pyfortress.test', 'pyfortress.util'],
      #packages=find_packages(exclude=['pyfortress.env', 'pyfortress.file']),      

      package_data={
        # If any package contains *.txt or *.rst files, include them:
        '': ['*.md', '*.json'],
      },     
      
      install_requires=[
          'ldap3'
      ],      
      classifiers=[
        'Development Status :: 3 - Alpha',
        'Programming Language :: Python :: 3',  
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Topic :: Security',
        'Topic :: Software Development :: Libraries :: Application Frameworks',
        'Topic :: Software Development :: Libraries :: Python Modules',          
      ],
      keywords='authorization rbac security', 
      #namespace_packages=['pyfortress'],
      entry_points={
       'console_scripts': [
           'initldap = pyfortress.test.test_dit_dao:main',
           'cli = pyfortress.test.cli:main',
           'clitest = pyfortress.test.cli_test_auth:main',           
        ],
      },           
      zip_safe=False)