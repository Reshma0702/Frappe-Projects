from setuptools import setup, find_packages

with open("requirements.txt") as f:
	install_requires = f.read().strip().split("\n")

# get version from __version__ variable in onedata/__init__.py
from onedata import __version__ as version

setup(
	name="onedata",
	version=version,
	description="onedata assesment",
	author="onedata solutions",
	author_email="onedata@gmail.com",
	packages=find_packages(),
	zip_safe=False,
	include_package_data=True,
	install_requires=install_requires
)
