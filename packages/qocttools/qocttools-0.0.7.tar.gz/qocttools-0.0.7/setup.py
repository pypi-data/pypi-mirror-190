import setuptools
from Cython.Build import cythonize

with open("README.rst", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    long_description=long_description,
    long_description_content_type="text/x-rst",
    packages=setuptools.find_packages(),
    ext_modules = cythonize("qocttools/cythonfuncs.pyx", language_level = 3)
)

