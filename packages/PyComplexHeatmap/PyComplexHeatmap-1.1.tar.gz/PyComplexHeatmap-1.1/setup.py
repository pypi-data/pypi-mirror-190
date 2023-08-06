# -*- coding: utf-8 -*-
"""
Created on Thu may 5 11:27:17 2022

@author: DingWB
"""

try:
    from setuptools import setup,find_packages
except ImportError:
    from distutils.core import setup,find_packages

setup(
   name='PyComplexHeatmap',
   version='1.01',
   description='A Python package to plot complex heatmap',
   author='Wubin Ding',
   author_email='ding.wu.bin.gm@gmail.com',
   url="https://github.com/DingWB/PyComplexHeatmap",
   # packages=['PyComplexHeatmap'],
   package_dir={'':'PyComplexHeatmap'},
   packages=find_packages('PyComplexHeatmap'),
   install_requires=['matplotlib>=3.3.1','pandas'],
   data_files=[('Lib/site-packages/PyComplexHeatmap/data',['data/mammal_array.pkl'])]
   #scripts=['scripts/PyComplexHeatmap'],
)
