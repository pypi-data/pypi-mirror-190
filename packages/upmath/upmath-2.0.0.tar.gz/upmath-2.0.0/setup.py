from setuptools import setup, find_packages

# read the contents from README file
from os import path
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
  name='upmath',
  version='2.0.0',
  description='This package creates upnumber (universal precisional number) which can create \
  flaoting and fractional numbers of bases 2, 8, 10, 16, 32, and 64. That is why, they are \
  called universal numbers. This number system can create accurate number with any level of \
  precision set by the user. There are 42 standard math functions for scientific calculations. \
  So, this package is named as\
  upmath (universal precision mathematics).',
  long_description=long_description,
  long_description_content_type='text/markdown',
  url='',
  author='A K M Aminul Islam',
  author_email='aminul71bd@gmail.com',
  maintainer='A K M Aminul Islam',
  maintainer_email='aminul71bd@gmail.com',
  license='NEWTONIA FREEWARE LICENSE',
  packages=find_packages(),
  py_modules=['upmath.src.digits','upmath.src.mypi','upmath.src.pE',\
'upmath.src.psmf','upmath.src.upnumber'],
  data_files = [("", ["LICENSE"])],
  zip_safe=False
)
