
# This file is essential if you intend to build the actual module
# It contains information about your package, specifically the name of the package, its version, platform-dependencies and a whole lot more.

from setuptools import setup, find_packages
import setuptools

with open("README.md", "r") as f:
	description = f.read()

setuptools.setup(
	name="my_minipack",
	version="1.0.1",
	author="esommier",
	author_email="esommier@student.42.fr",
	# packages=["my_minipack"],
	description="How to create a package in python.",
	long_description=description,
	long_description_content_type="text/markdown",
	# url="[PATH TO BOOTCAMP PYTHON]/module02/tmp_env/lib/python3.7/site-packages",
	license='GPLv3',
	package_dir={"": "src"},
	packages=setuptools.find_packages(where="src"),
	python_requires='>=3.8',
	install_requires=[],
	classifiers=[
		"Development Status :: 3 - Alpha",
		"Intended Audience :: Developers",
		# "Intended Audience :: Students",
		"Topic :: Education",
		# "Topic :: HowTo",
		# "Topic :: Package",
		"License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
		"Programming Language :: Python :: 3",
		"Programming Language :: Python :: 3 :: Only",
	],
)