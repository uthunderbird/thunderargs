from setuptools import setup
from os.path import join, dirname
from thunderargs import __version__


setup(
    name='thunderargs',
    version=__version__,
    license='JSON license',
    description='Let you use function annotations (PEP 3107) to parse'
                'and validate arguments',
    packages=['thunderargs'],
    url='https://bitbucket.org/dsupiev/thunderargs',
    long_description=open(join(dirname(__file__), 'README.rst')).read(),
    author="uthunderbird",
    author_email="undead.thunderbird@gmail.com",
)