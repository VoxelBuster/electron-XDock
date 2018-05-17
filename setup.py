from distutils.core import setup
import py2exe

NAME = 'holodock'
DESCRIPTION = 'Dock app written in Python and Java with a hologram look and feel.'
URL = 'https://github.com/VoxelBuster/winX-holo-dock'
EMAIL = 'voxelbustergaming@gmail.com'
AUTHOR = 'Galen Nare'
REQUIRES_PYTHON = '>=2.7.1'
VERSION = 'RC-0.2'

setup(name=NAME,
    version=VERSION,
    description=DESCRIPTION,
    author=AUTHOR,
    author_email=EMAIL,
    python_requires=REQUIRES_PYTHON,
    url=URL,
    console=['electronUI.py'])