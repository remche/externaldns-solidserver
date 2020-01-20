# -*- coding: utf-8 -*-
from setuptools import setup, find_packages

setup(
    name='externaldns-solidserver',
    version='0.1',

    description='External DNS implemtation for EfficientIP SolidServer',

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
