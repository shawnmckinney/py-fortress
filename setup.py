'''
@copyright: 2022 - Symas Corporation
'''
from setuptools import setup
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(name='py-fortress',
      version='0.1.1',
      python_requires='>=3.6',
      description='RBAC for Python',
      long_description=long_description,
      long_description_content_type="text/markdown",
      url='https://github.com/shawnmckinney/py-fortress',
      author='Symas Corporation',
      author_email='smckinney@symas.com,ebackes@symas.com',
      license='Apache License 2.0',      
      packages=['rbac', 'rbac.cli', 'rbac.ldap', 'rbac.model', 'rbac.util', 'rbac.tests', 'doc'],
      package_data={
        # If any package contains *.txt or *.rst files, include them:
        '': ['*.md', '*.json'],
      },     
      
      install_requires=[
          'python-ldap >= 3.4.0',
          'six',
          'ldappool >= 3.0.0'
      ],
      classifiers=[
        'Development Status :: 4 - Beta',
        'Programming Language :: Python :: 3',  
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Topic :: Security',
        'Topic :: Software Development :: Libraries :: Application Frameworks',
        'Topic :: Software Development :: Libraries :: Python Modules',          
      ],
      keywords='authorization rbac security', 
      #namespace_packages=['src'],
      entry_points={
       'console_scripts': [
           'initldap = rbac.tests.test_dit_dao:main',
           'cli = rbac.cli.cli:main',
           'clitest = rbac.cli.cli_test_auth:main',
        ],
      },           
      zip_safe=False)
