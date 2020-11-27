# -*- coding: utf-8 -*-
from setuptools import setup, find_packages
from os import path
import sys

if sys.version_info >= (3, 0):
    directory = path.abspath(path.dirname(__file__))
    with open(path.join(directory, 'README.md'), encoding='utf-8') as f:
        long_description = f.read()

setup(
    name='externaldns-solidserver',
    version='0.1.4',

    description='External DNS implemtation for EfficientIP SolidServer',
    long_description=long_description,
    long_description_content_type='text/markdown',

    author='Rémi Cailletaud',
    author_email='remche@remche.org',

    url='https://gricad-gitlab.univ-grenoble-alpes.fr/gricad/openstack/\
    externaldns-solidserver/blob/master/driver.py',

    classifiers=['Development Status :: 3 - Alpha',
                 'License :: OSI Approved :: Apache Software License',
                 'Programming Language :: Python',
                 'Programming Language :: Python :: 2',
                 'Programming Language :: Python :: 2.7',
                 'Programming Language :: Python :: 3',
                 'Programming Language :: Python :: 3.5',
                 'Intended Audience :: Developers',
                 'Environment :: Console',
                 ],

    platforms=['Any'],

    scripts=[],

    provides=['neutron.services.externaldns.drivers.solidserver',
              ],

    packages=find_packages(),

    entry_points={
        'neutron.services.external_dns_drivers': [
            'solidserver = solidserver.driver:SolidServer',
        ],
    },

    zip_safe=False,
)
