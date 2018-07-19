from setuptools import setup, find_packages

with open('README.md') as f:
    LONG_DESCRIPTION = f.read()

setup(name='dwdopen',
      version='0.1',
      author='David M. Straub',
      author_email='david.straub@tum.de',
      description='Python library to access DWD Open Data from https://opendata.dwd.de',
      long_description=LONG_DESCRIPTION,
      long_description_content_type='text/markdown',
      license='MIT',
      packages=find_packages(),
    )
