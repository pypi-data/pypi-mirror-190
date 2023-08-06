from setuptools import setup, find_packages



long_description = 'Library for working with projectZ. Write your chat bots, PR bots and more!'
link = 'https://github.com/xXxCLOTIxXx/projectZ.py/archive/refs/heads/main.zip'
ver = '1.0'

setup(
	name = "projectZ.py",
	version = ver,
	url = "https://github.com/xXxCLOTIxXx/projectZ.py",
	download_url = link,
	license = "MIT",
	author = "Xsarz",
	author_email = "xsarzy@gmail.com",
	description = "Library for creating projectZ bots and scripts.",
	long_description = long_description,
	keywords = [
		"projectZ.py",
		"projectZ",
		"projectZ-py",
		"projectZ-bot",
		"api",
		"python",
		"python3",
		"python3.x",
		"xsarz",
		"official"
	],
	install_requires = [
		"colored",
		"requests",

	],
	packages = find_packages()
)
