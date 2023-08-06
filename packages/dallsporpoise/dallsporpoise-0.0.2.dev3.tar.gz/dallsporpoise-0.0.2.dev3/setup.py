# The setup script for installing dallsporpoise.
# from distutils.core import setup
from setuptools import setup, find_packages
import os
import shutil

# Change this to True if you want to include the tests and test data
# in the distribution.
include_tests = False

try:
    # This deals with a bug where the tests aren't excluded due to not
    # rebuilding the files in this folder.
    shutil.rmtree('dallsporpoise.egg-info')
except OSError:
    pass

# Get the version info We do this to avoid importing __init__, which
# depends on other packages that may not yet be installed.
base_dir = os.path.abspath(os.path.dirname(__file__))
version = {}
with open(base_dir + "/dallsporpoise/_version.py") as fp:
    exec(fp.read(), version)


config = dict(
    name='dallsporpoise',
    version=version['__version__'],
    description='Lightweight fork of lkilchers dolfyn that parses corrupt 2019 vec files straight to netcdf.',
    author="iosonobert modifying lkilcher's dolfyn",
    author_email='',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: Apache Software License',
        'Natural Language :: English',
    ],
    url='http://github.com/iosonobert/dallsporpoise',
    packages=find_packages(exclude=['*.test']),

    package_data={},
    install_requires=['numpy', 'scipy', 'h5py', 'pyDictH5', 'netCDF4', 'pandas', 'xarray'],
    provides=['dallsporpoise', ],
    scripts=['scripts/motcorrect_vector.py', 'scripts/vec2mat.py'],
    # entry_points = {
    #    'console_scripts':
    #    ['motcorrect_vector = dolfyn.adv.scripts:motcorrect_vector',
    #     ],
    #    },
    dependency_links=['https://pypi.python.org/pypi/',
                      'https://github.com/lkilcher/pyDictH5/tarball/master#egg=pyDictH5'],
    # cmdclass =
    # {'install_data':chmod_install_data,'install':chmod_install,},
)


if include_tests:
    config['packages'].append('dallsporpoise.test')
    config['package_data'].update({'dallsporpoise.test': ['data/*']},)

setup(**config)
