# Change the content according to your package.
import setuptools
import re
import os

# Extract the version from the init file.
DATAFILE = "newpackage/__init__.py"
getversion = re.search(
    r"^__version__ = ['\"]([^'\"]*)['\"]", open(DATAFILE, "rt").read(), re.M)
if getversion:
    new_version = getversion.group(1)
else:
    raise RuntimeError("Unable to find version string in %s." % (DATAFILE,))

# Configurations
with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    install_requires=[
        'matplotlib',
        'numpy',
        'pandas'
    ],
    python_requires='>=3',
    name='newpackagewebforce',
    version=new_version,
    author="D.Mendez",
    author_email="pablomen1131@gmail.com",
    description="Python package for my newpackagewebforce.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/danielmen-mx/newpackagewebforce",
    download_url='https://github.com/danielmen-mx/newpackagewebforce/archive/'+new_version+'.tar.gz',
    packages=setuptools.find_packages(),
    include_package_data=True,
    license_files=["LICENSE"],
    classifiers=[
         "Programming Language :: Python :: 3",
         "License :: OSI Approved :: MIT License",
         "Operating System :: OS Independent",
    ],
)
