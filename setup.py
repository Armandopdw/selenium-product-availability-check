#!/usr/bin/env python

from distutils.core import setup

setup(name='El Corte Product Scrape',
      version='1.0',
      description='Python distribution to check sold-out items for restock',
      author='Armando Panman de Wit',
      author_email='armando.panmandewit@artlytic.nl',
      url='https://www.artlytic.nl/',
      packages=[],
      install_requires=[
          "beautifulsoup4>=4.9.2",
          "certifi>=2020.6.20",
          "chardet>=3.0.4",
          "idna>=2.10",
          "numpy>=1.19.2",
          "pandas>=1.1.2",
          "python-dateutil>=2.8.1",
          "pytz>=2020.1",
          "requests>=2.24.0",
          "selenium>=3.141.0",
          "six>=1.15.0",
          "soupsieve>=2.0.1",
          "urllib3>=1.25.10",
          "loguru>=0.5.3"
      ]
      )
