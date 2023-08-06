from distutils.util import convert_path

from setuptools import find_packages, setup
import pathlib

PACKAGE_DIR = "me_finder"

# Get the long description from the README file
here = pathlib.Path(__file__).parent.resolve()
long_description = (here / "README.md").read_text(encoding="utf-8")

setup(
    name="MobileElementFinder",
    version="1.1.1",
    description="Mobile Genetic Element prediction",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://bitbucket.org/mhkj/mge_finder/src/master/",
    author="Markus Johansson",
    author_email="markjo@food.dtu.dk",
    license="GPLv3",
    classifiers=[
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
    ],
    entry_points={"console_scripts": ["mefinder=me_finder.cli:cli"]},
    include_package_data=True,
    package_data={
        "me_finder": ["%s/logging.yml" % PACKAGE_DIR, "%s/config.ini" % PACKAGE_DIR]
    },
    packages=find_packages(exclude=("tests", "scripts")),
)
