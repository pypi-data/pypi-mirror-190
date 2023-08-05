# -*- encoding: UTF-8 -*-
import re
from os import path
from pathlib import Path
from typing import Generator

try:
    from setuptools import setup, find_packages
except ImportError:
    from distutils.core import setup
import io

CURRENT_FOLDER = Path(__file__).resolve().parent
REQUIREMENTS_PATH = CURRENT_FOLDER / "requirements.txt"

version_file = path.join(
    path.dirname(__file__),
    'src/as_flask_docs',
    '__init__.py'
)
with open(version_file, encoding="utf-8") as fp:
    m = re.search(
        r"^__version__ = ['\"]([^'\"]*)['\"]",
        fp.read(),
        re.M
    )
    version = m.groups(1)[0]

VERSION = version

with io.open("README.md", encoding='utf-8') as f:
    long_description = f.read()


def get_install_requires(req_file: Path = REQUIREMENTS_PATH) -> Generator[str, None, None]:
    with req_file.open("r") as f:
        for line in f:
            if line.startswith("#"):
                continue
            yield line.strip()


setup(
    name="as-flask-docs",
    version=VERSION,
    author="liuzhijun",
    author_email="lzjun567@gmail.com",
    url="https://github.com/Dorain-An/flask-docs",
    description="flask openapi(swagger) doc generator",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=["as_flask_docs"],
    package_data={
        'flask_docs': ['templates/*.html'],
    },
    include_package_data=True,
    license='MIT License',
    python_requires=">=3.6",
    install_requires=list(get_install_requires()),
    setup_requires=[
        'pytest-runner',
    ],
    tests_require=[
        "pytest",
    ],
    classifiers=[
        "Environment :: Web Environment",
        "Framework :: Flask",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Topic :: Internet :: WWW/HTTP :: Dynamic Content",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
)
