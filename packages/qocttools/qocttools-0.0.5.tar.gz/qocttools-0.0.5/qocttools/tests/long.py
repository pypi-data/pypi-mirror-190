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

import subprocess
import os
import tempfile
import shutil
import numpy as np
from distutils.dir_util import copy_tree
import pytest


def run_test(n, name = None, datafile = None):
    tempdir = tempfile.mkdtemp()
    if type(n) is int:
         n = str(n)
    dirname = os.path.dirname(__file__) + '/../sampleruns/' + n
    copy_tree(dirname, tempdir)
    cdir = os.getcwd()
    os.chdir(tempdir)
    if name is not None:
        fname = name
    else:
        fname = ' sample'+n
    i = subprocess.call('jupyter nbconvert ' + fname + '.ipynb --to python', shell = True)
    j = subprocess.call('python ' + fname +'.py', shell = True)
    datacomp = True
    if datafile is not None:
        data = np.loadtxt(datafile)
        dataref = np.loadtxt(datafile+'.ref')
        datacomp = (data == pytest.approx(dataref))
    os.chdir(cdir)
    if (i, j) == (0 , 0) and datacomp:
        shutil.rmtree(tempdir)
    else:
        print("Failed test directory at " + tempdir)
    return i, j, datacomp


def test_qocttoffoli():
    i, j, datacomp = run_test('qocttoffoli', name = 'qocttoffoli', datafile = 'data')
    assert  (i, j) == (0, 0) and datacomp


# This file should be run as "pytest -v long.py"
# Or, even better: "pytest -n NPROCS --durations=0 -v long.py"
# where NPROCS is the number of cores that can be used in parallel.
