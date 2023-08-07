from setuptools import setup

setup(
   name='aussrc-clients',
   version='0.1.0',
   author='Dave Palot',
   author_email='dave.pallot@uwa.edu.au',
   packages=['aussrc'],
   install_requires=[
       "aiohttp",
   ],
)