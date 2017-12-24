import os
from setuptools import setup

# Utility function to read the README file.
# Used for the long_description.  It's nice, because now 1) we have a top level
# README file and 2) it's easier to type in the README file than to put a raw
# string in below ...
def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name = "uip-scrape",
    version = "0.0.1",
    author = "Abhay Raizada",
    author_email = "toabhayraizada@gmail.com",
    description = ("A library to write image scraping plugins and" 
                    "running them to return a list of image_links"),
    license = "MIT",
    keywords = "python image scraping library",
    url = "",
    packages=['lib', 'tests'],
    long_description=read('README.md'),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Topic :: Utilities",
        "License :: OSI Approved :: MIT License",
    ],
)