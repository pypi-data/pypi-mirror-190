import pathlib
from setuptools import find_packages, setup

HERE = pathlib.Path(__file__).parent

VERSION = '1.0.2' 
PACKAGE_NAME = 'Quickdata' 
AUTHOR = 'Diego Alejandro Ramírez Araujo' 
AUTHOR_EMAIL = 'daramireza11@gmail.com' 
URL = 'https://github.com/Diegoramirez1999/Quickdata' 

LICENSE = 'MIT' 
DESCRIPTION = 'Automatizar labores presentes en el día a día de los Data Scientists.' 
LONG_DESCRIPTION = (HERE / "README.md").read_text(encoding='utf-8') 
LONG_DESC_TYPE = "text/markdown"

setup(
    name=PACKAGE_NAME,
    version=VERSION,
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    long_description_content_type=LONG_DESC_TYPE,
    author=AUTHOR,
    author_email=AUTHOR_EMAIL,
    url=URL,
    license=LICENSE,
    packages=find_packages(),
    include_package_data=True
)