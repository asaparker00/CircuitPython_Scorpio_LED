from setuptools import setup
from setuptools import find_packages
import os

setup(
    name='cp_led_strip',
    version='0.1.0',
    description='Library for sending and receiving messages to a rp2040 using circuitpython',
    long_description=__doc__,
    author='Asa Parker and Will Dickson',
    author_email='parkeasa@oregonstate.edu',
    license='MIT',

    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],

    packages=find_packages(exclude=['examples',]),
)
