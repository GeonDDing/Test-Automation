from setuptools import setup, find_packages

### setup.py exceute command 
### pip install -e .

setup(
    name='example',
    version='0.1.0',
    packages=find_packages(include=['Common', 'Common.*', 'API', 'API.*', 'WebTesting', 'WebTesting.*'])
)

