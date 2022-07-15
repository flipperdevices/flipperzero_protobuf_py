

import os.path
from setuptools import setup, find_packages
from distutils.command.install_scripts import install_scripts
import ssl
# from version import tag_version

# ssl._create_default_https_context = ssl._create_unverified_context
# python setup.py sdist  -k -v  --dry-run

# python setup.py --dry-run --verbose install
# python setup.py install --record files.txt

from distutils.core import setup

version = '0.1.20220714'

setup(
    name='flipperzero_protobuf',
    version=version,
    # author='Peter Shipley',
    author_email='Peter.Shipley@gmail.com',
    packages=['flipperzero_protobuf', 'flipperzero_protobuf/flipperzero_protobuf_compiled'],
    # packages=find_packages(),
    # scripts=['flipperzero_cmd.py'],
    url='https://github.com/evilpete/flipperzero_protobuf_py',
    git='https://github.com/evilpete/flipperzero_protobuf_py.git',
    classifiers=[
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 3 - Alpha',

        # Indicate who your project is intended for
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',

        # Pick your license as you wish (should match "license" above)
        # 'License :: OSI Approved :: MIT License',

        # Specify the Python versions you support here. In particular, ensure
        # that you indicate whether you support Python 2, Python 3 or both.
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
    python_requires='>=3',

    license='BSD',
    # download_url='https://bitbucket.org/evilpete/scapy-watch/get/master.tar.gz',
    description='Python API wrapper for flipperzero_protobuf.',
    # long_description=open('README.txt').read(),
    # cmdclass = { 'install_scripts': install_scripts_and_symlinks }
    install_requires=['numpy==1.22.3', 'protobuf==3.20.1', 'protoletariat'],
    entry_points={
           'console_scripts': [
               'flipperzero_cmd = flipperzero_protobuf.flipperzero_cmd:main'
          ],
      }
)

