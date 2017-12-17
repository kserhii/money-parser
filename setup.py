import re
import sys
import pathlib

from setuptools import setup


NAME = 'money-parser'
DESCRIPTION = 'Price and currency parsing utility'
URL = 'https://github.com/kserhii/money-parser'

AUTHOR = 'Serhii Kostel'
EMAIL = 'dodge.ksv@gmail.com'


# ------------------------------------------------

here = pathlib.Path(__file__).parent
version_file = here / 'money_parser' / '__init__.py'
readme_file = here / 'README.rst'
changes_file = here / 'CHANGES.rst'


def read(file):
    with file.open(encoding='utf8') as f:
        return f.read().strip()


try:
    version = re.findall(r"^__version__ = '([^']+)'$", read(version_file), re.M)[0]
except IndexError:
    raise RuntimeError('Unable to determine version.')


long_description = read(readme_file) + '\n\n' + read(changes_file)


needs_pytest = {'pytest', 'test', 'ptr'}.intersection(sys.argv)
if needs_pytest:
    setup_requires = ['pytest-runner']
else:
    setup_requires = []


setup(
    name=NAME,
    version=version,
    description=DESCRIPTION,
    long_description=long_description,
    author=AUTHOR,
    author_email=EMAIL,
    url=URL,
    packages=['money_parser'],
    include_package_data=True,
    setup_requires=setup_requires,
    tests_require=['pytest'],
    license='Apache 2',
    python_requires='>=3.4',
    classifiers=[
        'License :: OSI Approved :: Apache Software License',
        'Intended Audience :: Developers',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Topic :: Text Processing',
        'Topic :: Text Processing :: General'
    ],
)
