from setuptools import setup, find_packages

VERSION = '0.0.3'
DESCRIPTION = 'Mojo RPG test game'
LONG_DESCRIPTION = 'A package demonstrates mojo rpg combat'

setup(
    name="mojoRPG",
    version=VERSION,
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    author="Alex Iannicelli",
    author_email="atiannicelli@gmail.com",
    license='MIT',
    packages=find_packages(),
    install_requires=[],
    keywords='mojo',
    classifiers= [
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        'License :: OSI Approved :: MIT License',
        "Programming Language :: Python :: 3",
    ]
)
