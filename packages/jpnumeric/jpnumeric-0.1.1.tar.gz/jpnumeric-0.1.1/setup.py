#!python3
from setuptools import setup

DESCRIPTION = 'jpnumberic: convert japanese-numeral string and integer.'
NAME = 'jpnumeric'
AUTHOR = 'hideto honda'
AUTHOR_EMAIL = 'honda.alfa@gmail.com'
URL = 'https://zenn.dev/karamawanu'
LICENSE = 'MIT'
DOWNLOAD_URL = URL
VERSION = '0.1.1'
PYTHON_REQUIRES = '>=3.6'
INSTALL_REQUIRES = []
PACKAGES = [
    NAME
]
KEYWORDS = 'kanji japanese numerals interger'
CLASSIFIERS=[
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3.6'
]
README = open("README.md").read()
LONG_DESCRIPTION = README
LONG_DESCRIPTION_CONTENT_TYPE = 'text/markdown'

setup(
    name=NAME,
    version=VERSION,
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    long_description_content_type=LONG_DESCRIPTION_CONTENT_TYPE,
    author=AUTHOR,
    author_email=AUTHOR_EMAIL,
    maintainer=AUTHOR,
    maintainer_email=AUTHOR_EMAIL,
    url=URL,
    download_url=URL,
    packages=PACKAGES,
    classifiers=CLASSIFIERS,
    license=LICENSE,
    keywords=KEYWORDS,
    install_requires=INSTALL_REQUIRES
)
