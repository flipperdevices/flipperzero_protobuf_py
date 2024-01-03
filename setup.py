import os.path
import ssl
from distutils.command.install_scripts import install_scripts

from setuptools import find_packages, setup

# from version import tag_version

# ssl._create_default_https_context = ssl._create_unverified_context
# python setup.py sdist  -k -v  --dry-run

# python setup.py --dry-run --verbose install
# python setup.py install --record files.txt

# from distutils.core import setup

version = "0.1.20221108"

exec(open("./flipperzero_protobuf/version.py").read())

setup(
    name="flipperzero_protobuf",
    version=version,
    author="Flipper & Community",
    author_email="peter.shipley@gmail.com, hello@flipperzero.one",
    packages=[
        "flipperzero_protobuf",
        "flipperzero_protobuf/flipperCmd",
        "flipperzero_protobuf/flipperzero_protobuf_compiled",
    ],
    url="https://github.com/evilpete/flipperzero_protobuf_py",
    git="https://github.com/evilpete/flipperzero_protobuf_py.git",
    classifiers=[
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        "Development Status :: 3 - Alpha",
        # Indicate who your project is intended for
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Build Tools",
        "License :: OSI Approved :: BSD License",
        # Specify the Python versions you support here. In particular, ensure
        # that you indicate whether you support Python 2, Python 3 or both.
        "Programming Language :: Python :: 3",
    ],
    python_requires=">=3",
    license="BSD",
    # download_url='https://github.com/flipperdevices/flipperzero_protobuf_py/archive/refs/heads/main.zip',
    description="Python API wrapper for flipperzero_protobuf.",
    # long_description=open('README.txt').read(),
    # cmdclass = { 'install_scripts': install_scripts_and_symlinks }
    install_requires=[
        'pyreadline; platform_system == "Windows"',
        "protobuf==3.20.2",
        "pyserial",
    ],
    entry_points={
        "console_scripts": [
            "flipperCmd = flipperzero_protobuf.flipperCmd.flipperzero_cmd:main"
        ],
    },
)
