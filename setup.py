from setuptools import setup, find_packages

setup(
    name='kaggle-lib',
    version='0.2',
    description='Lib for kaggle',
    author='Uiqkos',
    packages=['kaggle_lib'],
    install_requires=['kaggle', 'pandas'],
)