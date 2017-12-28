import sys
import setuptools

from setuptools import setup
from setuptools.command.test import test as TestCommand


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
        import os
        import shutil

        tar_file = 'sample.tar.gz'

        if os.path.exists(tar_file):
            if os.path.exists('sample'):
                shutil.rmtree('sample')

            shutil.unpack_archive(tar_file)
        else:
            print(f'File not found: {tar_file}')
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
)

setup(**config)

