from setuptools import setup, find_packages

setup(name='coderadar',
      version='0.4.1',
      packages=find_packages(),
      entry_points = {
          'console_scripts': ['coderadar=coderadar.__main__:main'],
          }
     )
