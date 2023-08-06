from distutils.core import  setup
import setuptools
packages = ['hidewavinjpg']# 唯一的包名，自己取名
setup(name='hidewavinjpg',
	version='1.4',
	author='gdxy',
    packages=packages, 
    package_dir={'requests': 'requests'},)
