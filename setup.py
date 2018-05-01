from setuptools import setup
import os

with open('version.txt') as file:
    version = file.read().strip()

resources = os.path.join('config', '*.yaml')

setup(name='horoscope_scraper',
      version=version,
      description='Get horoscope readings from different sources',
      author='Jonathon Carlyon',
      author_email='JonathonCarlyon@gmail.com',
      url='https://github.com/JonnyFb421',
      install_requires=[''],
      extras_require={'dev': ['pytest']},
      packages=['horoscope_scraper'],
      package_data={'horoscope_scraper': [resources]},
      )
