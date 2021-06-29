from setuptools import setup, find_packages

with open('requirements.txt', 'r') as f:
    requirements = f.read().split('\n')

setup(
    name='dicepy',
    version='0.0.1',
    author='Nonowazu',
    author_email='oowazu.nonowazu@gmail.com',
    description='A small dice rolling library',
    python_requires='>=3.7',
    packages=find_packages(),
)
