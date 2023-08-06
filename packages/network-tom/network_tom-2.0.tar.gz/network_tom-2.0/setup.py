from setuptools import setup, find_packages

build_options = {'packages': [], 'excludes': []}

setup(
    name='network_tom',
    version='2.0',
    packages=find_packages(),
    options = {'build_exe': build_options},
    entry_points={
        'console_scripts': [
        'hah = hah:main',
        ],
    },

)
