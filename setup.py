import os

from setuptools import setup, find_packages

HERE = os.path.abspath(os.path.dirname(__file__))
PATH_VERSION = os.path.join(HERE, 'fmm', '__version__.py')

ABOUT = {}
with open(PATH_VERSION, mode='r', encoding='utf-8') as f:
    exec(f.read(), ABOUT)


setup(
    name=ABOUT['__title__'],
    version=ABOUT['__version__'],
    description=ABOUT['__description__'],
    packages=find_packages(
        exclude=['*.test']
    ),
    entry_points='''
        [console_scripts]
        ci=ci.cli:cli
    '''
)
