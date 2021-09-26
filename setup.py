from setuptools import setup, find_packages
import sys
from os import path
from src.version import __version__  # pylint: disable=relative-beyond-top-level

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()


setup(
    name='geneMatcher',
    version=__version__,
    description = "geneMatcher sequence clustering software.",
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/DBRetina/geneMatcher',
    author='Mohamed Abuelanin (UC Davis), Tamer Mansour (UC Davis)',
    author_email='mabuelanin@gmail.com, drtamermansour@gmail.com',
    keywords='genes databases genome transcriptomes',
    python_requires='>=3.6',
    install_requires=[
        'Click',
        'kProcessor==1.2.0',
        'kSpider2',
        'tqdm',
        'requests'
    ],
    entry_points={
        'console_scripts': [
            'geneMatcher=src.geneMatcher:cli',
        ],
    },
    packages=find_packages(),
    include_package_data=True,
    project_urls={
        'Bug Reports': 'https://github.com/mr-eyes/geneMatcher/issues',
        'Say Thanks!': 'https://saythanks.io/to/mr-eyes',
        'Source': 'https://github.com/mr-eyes/geneMatcher',
        },
)