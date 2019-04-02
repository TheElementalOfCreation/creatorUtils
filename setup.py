import setuptools;

with open("README.md", "r") as fh:
	long_description = fh.read();

with open("LICENSE", "r") as fh:
	li = fh.read();

setuptools.setup(
	name = "creatorUtils",
	version = "0.2.5",
	author = "The Elemental of Creation",
	author_email = "arceusthe@gmail.com",
	description = "creatorUtils main package",
	long_description = long_description,
	url = "https://github.com/TheElementalOfCreation/creatorUtils",
	packages = setuptools.find_packages(),
	license = li,
	classifiers = (
		"Programming Language :: Python",
		"Programming Language :: Python :: 2",
		"Programming Language :: Python :: 2.7",
		"Programming Language :: Python :: 3",
		"Programming Language :: Python :: 3.4",
		"Programming Language :: Python :: 3.5",
		"Programming Language :: Python :: 3.6",
		"Programming Language :: Python :: Implementation :: CPython",
		"Programming Language :: Python :: Implementation :: PyPy",
		"License :: OSI Approved :: MIT License",
		"Operating System :: OS Independent",
	),
);
