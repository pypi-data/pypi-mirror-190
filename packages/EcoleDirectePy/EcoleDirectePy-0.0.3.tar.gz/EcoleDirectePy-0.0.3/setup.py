from setuptools import setup, find_packages
import codecs
import os


VERSION = '0.0.3'
DESCRIPTION = 'a API Wrapper for EcoleDirecte.fr'

# Setting up
setup(
    name="EcoleDirectePy",
    version=VERSION,
    author="DK16",
    author_email="<dk16v2@gmail.com>",
    description=DESCRIPTION,
    packages=find_packages(),
    install_requires=['requests'],
    keywords=['python', 'ecoledirecte', 'api', 'Wrapper'],
)