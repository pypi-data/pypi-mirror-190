import os.path

from setuptools import find_packages
from setuptools import setup

path = os.path.relpath(os.path.dirname(__file__))

setup(
    author='Andy Stokely',
    email='amstokely@ucsd.edu',
    name='pycautodoc',
    install_requires=[],
    platforms=['Linux',
               'Unix', ],
    python_requires=">=3.8",
    py_modules=[path + "pycautodoc/pycautodoc"],
    packages=find_packages() + [''],
    zip_safe=False,
    package_data={
        '': [
            path + '/pycautodoc/_pycautodoc.so'
        ]
    },
)
