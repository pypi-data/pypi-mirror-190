## Copyright 2019-present The qocttools developing team
##
## This file is part of qocttools.
##
## qocttools is free software: you can redistribute it and/or modify
## it under the terms of the GNU General Public License as published by
## the Free Software Foundation, either version 3 of the License, or
## (at your option) any later version.
##
## qocttools is distributed in the hope that it will be useful,
## but WITHOUT ANY WARRANTY; without even the implied warranty of
## MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
## GNU General Public License for more details.
##
## You should have received a copy of the GNU General Public License
## along with qocttools.  If not, see <https://www.gnu.org/licenses/>.



import os
import pkg_resources  # part of setuptools
from gitinfo import get_git_info
import pytest


def isnotebook():
    """Returns True if running within a notebook, False otherwise"""
    try:
        shell = get_ipython().__class__.__name__
        if shell == 'ZMQInteractiveShell':
            return True   # Jupyter notebook or qtconsole
        elif shell == 'TerminalInteractiveShell':
            return False  # Terminal running IPython
        else:
            return False  # Other type (?)
    except NameError:
        return False      # Probably standard Python interpreter


def about():
    """Prints about information about the version

    If available, it also prints out the git hash
    """
    version = pkg_resources.require("qocttools")[0].version
    print("Running qocttools version "+version)
    gitdir = os.path.dirname(__file__)+'/..'
    git_info = get_git_info(gitdir)
    if git_info is not None:
        print("    Project repository git hash = " + git_info["commit"])
        print("    Project repository last commit date = " + git_info["author_date"])
        print("    Project repository refs = " + git_info["refs"])


def test():
    """Runs the testsuite (the short one)"""
    print("Running qocttools testsuite")
    testsuite_dir = os.path.join(os.path.dirname(__file__), '../tests')
    pytest.main(["-v", os.path.join(testsuite_dir, "short.py")])
