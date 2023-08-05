import setuptools
from Cython.Build import cythonize

with open("README.rst", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="qocttools", # Replace with your own username
    version="0.0.3",
    author="Alberto Castro",
    author_email="alberto.castro.barrigon@gmail.com",
    description="A set of tools to do quantum optimal control in combination with the QuTIP package",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://acbarrigon.gitlab.io/qocttools/",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: GNU GENERAL PUBLIC LICENSE Version 3",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.9',
    ext_modules = cythonize("qocttools/cythonfuncs.pyx", language_level = 3)
)

