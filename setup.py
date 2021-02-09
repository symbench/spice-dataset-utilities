import os
from setuptools import setup

with open(os.path.join('.', 'requirements.txt')) as f:
    install_deps = [ line.strip() for line in f.readlines() ]

setup(name='spice_dataset_utilities',
      version='0.0.1',
      description='Utilities for netlist datasets',
      author='Brian Broll',
      author_email='brian.broll@vanderbilt.edu',
      install_requires=install_deps,
      license='MIT',
      packages=['spice_dataset_utilities'],
      zip_safe=False)
