from setuptools import setup
import os

with open('README.MD', 'rt') as arq:
      readme = arq.read()

keywords = ['EventSimpleGUI']

setup(name='EventSimpleGUI',
      version='0.1.9',
      license='MIT license',
      author='Daniel Coêlho',
      long_description=readme,
      long_description_content_type='text/markdown',
      author_email='heromon.9010@gmail.com',
      keywords=keywords,
      description='A simple tool to create events to PySimpleGUI',
      packages=['pysimpleevent'],
      install_requires=['PySimpleGUI']
)