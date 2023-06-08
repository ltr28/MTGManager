from setuptools import setup, find_packages

VERSION = '0.0.1' 
DESCRIPTION = 'My first Python package'
LONG_DESCRIPTION = 'My first Python package with a slightly longer description'

# Setting up
setup(
       # the name must match the folder name 'verysimplemodule'
        name="ManageMTG", 
        version=VERSION,
        author="Luke Trenberth",
        author_email="<luketrenberth@gmail.com>",
        description=DESCRIPTION,
        long_description=LONG_DESCRIPTION,
        packages=find_packages(),
        install_requires=[
            'fastparquet',
            'pandas',
            'pyarrow',
            'pylint',
            'pytest',
            'requests',
            ],
        python_requires='>=3.7'
)