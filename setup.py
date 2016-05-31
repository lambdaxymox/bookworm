try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

config = {
    'description': 'Bookworm',
    'author': 'Stallmanifold',
    'url': '',
    'download_url': '',
    'author_email': 'stallmanifold@gmail.com',
    'version': '0.1',
    'install_requires': ['nose'],
    'packages': ['bookworm'],
    'scripts': [],
    'name': 'bookworm'
}

setup(**config)