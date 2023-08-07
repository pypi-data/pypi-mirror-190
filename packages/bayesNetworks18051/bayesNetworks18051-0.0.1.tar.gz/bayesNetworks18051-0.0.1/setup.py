from setuptools import setup, find_packages
import codecs
import os


VERSION = '0.0.1'
DESCRIPTION = 'simple library for bayesian networks'
LONG_DESCRIPTION = 'A package that allows you to create bayesian networks and perform certain actions on them'

# Setting up
setup(
    name="bayesNetworks18051",
    version=VERSION,
    author="Javier Alvarez",
    author_email="<javieremilio1@gmail.com>",
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=['numpy'],
    keywords=['python', 'bayes', 'bayesian network'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)
