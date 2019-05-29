from setuptools import setup, find_packages
from codecs import open
from os import path
import os

working_dir = path.abspath(path.dirname(__file__))
ROOT = os.path.abspath(os.path.dirname(__file__))

# Read the README.
with open(os.path.join(ROOT, 'README.md'), encoding="utf-8") as f:
    README = f.read()

setup(name='spaghetti',
      version='0.0.1',
      description='',
      long_description=README,
      long_description_content_type='text/markdown',
      install_requires=["oyaml"],
)
