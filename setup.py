'''
Created on Apr 4, 2018

@author: smckinn
@copyright: 2018 - Symas Corporation
'''
from setuptools import setup, find_packages

# To use a consistent encoding
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(name='py-fortress',
      version='0.0.1',
      python_requires='>=3',
      description='RBAC for Python',
      long_description=long_description,
      long_description_content_type="text/markdown",
      url='https://github.com/shawnmckinney/py-fortress',
      author='Symas Corporation',
      author_email='smckinney@symas.com,ebackes@symas.com',
      license='Apache License 2.0',      
      packages=['pyfortress.doc', 'pyfortress.impl', 'pyfortress.ldap', 'pyfortress.model', 'pyfortress.test', 'pyfortress.util'],
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
      zip_safe=False)





















      #include_package_data=False,
      #packages=find_packages(exclude=['py-fortress.env','py-fortress.test', 'env', '*.log']),
      #packages=['py-fortress.impl', 'py-fortress.ldap', 'py-fortress.model', 'py-fortress.util'],
      #packages=['py-fortress.impl'],
      #packages=find_packages(exclude=["*.test", "*.test.*" '*.env', '*.env.*']),
      #include_package_data=True,
      #include_package_data=False,
      #package_data={
        # If any package contains *.txt or *.rst files, include them:
        #'': ['*.txt', '*.md', '*.json'],
       # 'py-fortress': ['*'],
       # 'py-fortress': ['test/*'],
      #},     
      #exclude_package_data={
      #  'py-fortress.test': ['*.log'],
      #  'py-fortress.env': ['*'],
      #  'py-fortress': ['env']      
      #},       
