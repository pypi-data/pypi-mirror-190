from setuptools import setup, find_packages

VERSION = '0.0.16'
DESCRIPTION = 'DES with Late Fusion'
LONG_DESCRIPTION = 'Implementation of Dynamic Ensemble Selection methods with Late Fusion'

setup(
    name="infodeslib",
    version=VERSION,
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    author='Firuz Juraev',
    author_email='f.i.juraev@gmail.com',
    license='MIT',
    packages=find_packages(),
    install_requires=[],
    keywords='conversion',
    classifiers= [
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        'License :: OSI Approved :: MIT License',
        "Programming Language :: Python :: 3",
    ]
)