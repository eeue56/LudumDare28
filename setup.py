#!/usr/bin/env python

from distutils.core import setup

setup(name='nigeludum',
      version='1.0.0.6',
      description='Ludum Dare game',
      author='Enalicho',
      author_email='enalicho@gmail.com',
      packages=['nigeludum', 'nigeludum/world_objects', 'nigeludum/levels', 'nigeludum/hivemind'],

      requires=['PyQt', 'OpenGL'],
     )