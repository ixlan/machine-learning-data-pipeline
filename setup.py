from setuptools import setup, find_packages
import os

with open('requirements.txt') as fp:
    install_requires = fp.read()

pack_path = 'mldp'
packages = [os.path.join(pack_path, p) for p in find_packages(pack_path)]

setup(
    name='machine_learning_data_pipeline',
    version='1.0.0',
    packages=[pack_path] + packages,
    long_description=open('README.md').read(),
    install_requires=install_requires
)
