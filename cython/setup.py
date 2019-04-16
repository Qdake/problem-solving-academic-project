#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Apr 14 18:38:53 2019

@author: wei
"""

from distutils.core import setup
from Cython.Build import cythonize
setup(ext_modules = cythonize("fonctions.pyx"))