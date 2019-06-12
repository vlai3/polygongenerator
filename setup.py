from setuptools import find_packages, setup

NAME = 'polygongenerator'
DESCRIPTION = 'Module for generating images of polygons'
VERSION = '0.0.1'
AUTHOR = 'Veronica Lai'

INSTALL_REQUIRES = [
    'opencv_python',
    'numpy',
    'pyqt5',
    'pyqt5-tools',
    'pyinstaller'
]

# find packages and prefix them with the main package name
PACKAGES = find_packages()

setup(
    name=NAME,
    version=VERSION,
    description=DESCRIPTION,
    author=AUTHOR,
    url='TODO',
    install_requires=INSTALL_REQUIRES,
    packages=PACKAGES,
    license='LICENSE',
)
