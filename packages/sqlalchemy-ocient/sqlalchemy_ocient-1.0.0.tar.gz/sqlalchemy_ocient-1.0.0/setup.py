import os
import pathlib
import sys
from typing import Dict

from setuptools import setup

# Get the long description from the README file
here: pathlib.Path = pathlib.Path(__file__).parent.absolute()
long_description = (here / "README.md").read_text(encoding="utf-8")

# Get the version from the version.py source file
version: Dict[str, str] = {}
if os.path.exists(os.path.join(here, "version.py")):
    with open(os.path.join(here, "version.py")) as version_file:
        exec(version_file.read(), version)
        VERSION = version["__version__"]
else:
    VERSION = "1.0.0"

setup(
    name="sqlalchemy_ocient",
    version=VERSION,
    description="Ocient for SQLAlchemy",
    long_description=long_description,
    long_description_content_type="text/markdown",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: Implementation :: CPython",
        "Topic :: Database :: Front-Ends",
    ],
    keywords="SQLAlchemy Ocient",
    author="Ocient Inc",
    author_email="info@ocient.com",
    install_requires=[
        "pyocient",
        "sqlalchemy",
    ],
    py_modules=["sqlalchemy_ocient", "version"],
    setup_requires=[
        "wheel",
    ],
    tests_require=["nose >= 0.11"],
    test_suite="nose.collector",
    entry_points={"sqlalchemy.dialects": ["ocient = sqlalchemy_ocient:OcientDialect"]},
    options={
        "bdist_wheel": {"universal": "1"},
        "pytest": {
            "addopts": "--tb native -v -r fxX",
            "python_files": "test/*test_*.py",
        },
        "nosetests": {
            "with-sqla_testing": "true",
            "where": "test",
            "cover-package": "sqlalchemy_ocientdb",
            "with-coverage": "1",
            "cover-erase": "1",
        },
        "sqla_testing": {
            "requirement_cls": "sqlalchemy_ocientdb.requirements:Requirements",
            "profile_file": ".profiles.txt",
        },
        "db": {
            "default": "ocientdb+pyodbc://admin@Test",
            "sqlite": "sqlite:///:memory:",
        },
    },
)
