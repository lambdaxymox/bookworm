import sys
import setuptools
import os

from setuptools import setup
from setuptools.command.test import test as TestCommand

TAR_FILE = os.path.join('tarballs', 'sample.tar.gz')
SAMPLE_ROOT = 'sample'


class PyTest(TestCommand):
    user_options = [('pytest-args=', 'a', "Arguments to pass to pytest")]

    def initialize_options(self):
        TestCommand.initialize_options(self)
        self.pytest_args = ''

    def run_tests(self):
        import shlex
        # Import here, because imports outside the eggs aren't loaded.
        import pytest
        errno = pytest.main(shlex.split(self.pytest_args))
        sys.exit(errno)


class InitializeSampleData(setuptools.Command):
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        import shutil

        if os.path.exists(TAR_FILE):
            if os.path.exists(SAMPLE_ROOT):
                shutil.rmtree(SAMPLE_ROOT)

            shutil.unpack_archive(TAR_FILE)
            sys.exit(0)
        else:
            print(f'File not found: {TAR_FILE}')
            sys.exit(1)


config = dict(
    description = 'Bookworm',
    author = 'Stallmanifold',
    url = 'https://github.com/stallmanifold/bookworm',
    download_url = 'https://github.com/stallmanifold/bookworm.git',
    author_email = 'stallmanifold@gmail.com',
    version = '0.1',
    install_requires = ['pytest', 'hypothesis'],
    license = "LICENSE-APACHE",
    package_dir = {'': 'src'},
    packages = ['bookworm'],
    scripts = [],
    name = 'bookworm',
    tests_require = ['pytest', 'hypothesis'],
    cmdclass = {
        'test': PyTest,
        'initialize_sample_data': InitializeSampleData
    },
    entry_points = {
        'console_scripts': [ 'bookworm = bookworm.bookworm.bookworm:main' ]
    }
)

setup(**config)

