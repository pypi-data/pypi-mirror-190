from setuptools import setup

# read the contents of your README file
from pathlib import Path
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(name='calculatortbalse',
      version='1.0',
      description='Calculator for Python Mastery project',
      long_description=long_description,
      long_description_content_type='text/markdown',
      author='Vienmarskinis',
      packages=['calculatortbalse', 'calculatortbalse/tests'],
      zip_safe=False)