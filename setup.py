from setuptools import setup
import os

with open('version.txt') as file:
    version = file.read().strip()

requirements = [
      'requests>=2.18.4',
      'scrapeit==1.0.2'
]
dev_requirements = [
      'pytest>=3.5.1'
]
resources = os.path.join('config', '*.yaml')

setup(name='horoscope_scraper',
      version=version,
      description='Get horoscope readings from different sources',
      author='Jonathon Carlyon',
      author_email='JonathonCarlyon@gmail.com',
      url='https://github.com/JonnyFb421',
      install_requires=requirements,
      extras_require={'dev': dev_requirements},
      packages=['horoscope_scraper'],
      package_data={'horoscope_scraper': [resources]},
      )
