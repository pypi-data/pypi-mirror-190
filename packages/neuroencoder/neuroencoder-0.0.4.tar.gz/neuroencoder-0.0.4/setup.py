from setuptools import setup

setup(
  name='neuroencoder',
  version='0.0.4',
  description='A package for processing temporal neural data, including spike trains, LFP, and EEG',
  url='https://github.com/avocardio/neuroencoder',
  author='M.K.',
  author_email='max@neuroencoder.com',
  packages=['neuroencoder'],
  long_description=open('README.md').read(),
  install_requires=[
    'numpy',
    'pyedflib',
    'tensorflow',
    'tqdm',
  ],
  classifiers=[
    'Development Status :: 2 - Pre-Alpha',
    'Intended Audience :: Healthcare Industry',
    'Intended Audience :: Science/Research',
    'License :: Other/Proprietary License',
    'Programming Language :: Python :: 3',
  ],
)