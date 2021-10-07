#!/bin/python3

import os
import re
from pathlib import Path

# https://github.com/google/skywater-pdk-libs-sky130_fd_sc_hs.git
# https://github.com/google/skywater-pdk-libs-sky130_fd_sc_hdll.git
# https://github.com/google/skywater-pdk-libs-sky130_fd_sc_ms.git
# https://github.com/google/skywater-pdk-libs-sky130_fd_sc_ls.git
# https://github.com/google/skywater-pdk-libs-sky130_fd_sc_lp.git
# https://github.com/google/skywater-pdk-libs-sky130_fd_sc_hvl.git
# https://github.com/google/skywater-pdk-libs-sky130_fd_io.git
# https://github.com/google/skywater-pdk-libs-sky130_fd_pr.git
#

def clone():
    os.system("git clone --recurse-submodules https://github.com/google/skywater-pdk-libs-sky130_fd_sc_hd.git")
    os.system("git clone --recurse-submodules https://github.com/google/skywater-pdk-libs-sky130_fd_sc_hdll.git")
    os.system("git clone --recurse-submodules https://github.com/google/skywater-pdk-libs-sky130_fd_sc_ms.git")
    os.system("git clone --recurse-submodules https://github.com/google/skywater-pdk-libs-sky130_fd_sc_ls.git")
    os.system("git clone --recurse-submodules https://github.com/google/skywater-pdk-libs-sky130_fd_sc_lp.git")
    os.system("git clone --recurse-submodules https://github.com/google/skywater-pdk-libs-sky130_fd_sc_hvl.git")
    os.system("git clone --recurse-submodules https://github.com/google/skywater-pdk-libs-sky130_fd_io.git")
    os.system("git clone --recurse-submodules https://github.com/google/skywater-pdk-libs-sky130_fd_pr.git")

def process(pathname, lefname) -> int:

    files = Path(pathname).rglob('*.lef')

    # filter out all the magic files
    files = [f for f in files if "magic" not in f.name]

    lefcontents = """
# Copyright 2020 The SkyWater PDK Authors
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# SPDX-License-Identifier: Apache-2.0
#
# Autogenerated by https://www.asicsforthemasses.com
#

VERSION 5.5 ;
NAMESCASESENSITIVE ON ;
BUSBITCHARS "[]" ;
DIVIDERCHAR "/" ;


"""

    NumberOfCells = 0
    print("Processing ...")
    for fn in files:
        print("    " + fn.name)

        with open(fn) as leffile:
            contents = leffile.read()

        leffile.close()

        start = 0
        stop  = 0

        p_macro = re.compile("MACRO ([a-z,0-9,_]*)")

        for macro in p_macro.finditer(contents):
            #print(macro.start(), macro.group(1))
            cellname = macro.group(1)
            start    = macro.start()

        p_end = re.compile("END "+cellname)

        for endmacro in p_end.finditer(contents):
            #print(endmacro.start(), endmacro.group())
            stop = endmacro.start() + len(endmacro.group())

        #print("    start", start, "stop", stop)

        if (start == stop):
            print("ERROR - could not find MACRO")
        else:
            celltxt = contents[start:stop]
            lefcontents += celltxt
            lefcontents += "\n\n\n"
            NumberOfCells += 1

    lefcontents += "END LIBRARY\n"

    f = open(lefname, "w")
    f.write(lefcontents)
    f.close()

    print("  number of cells:", NumberOfCells)

clone()
process('skywater-pdk-libs-sky130_fd_sc_hd', 'sky130_fd_sc_hd.lef')
process('skywater-pdk-libs-sky130_fd_sc_hdll', 'sky130_fd_sc_hdll.lef')
process('skywater-pdk-libs-sky130_fd_sc_ms', 'sky130_fd_sc_ms.lef')
process('skywater-pdk-libs-sky130_fd_sc_ls', 'sky130_fd_sc_ls.lef')
process('skywater-pdk-libs-sky130_fd_sc_lp', 'sky130_fd_sc_lp.lef')
process('skywater-pdk-libs-sky130_fd_sc_hvl', 'sky130_fd_sc_hvl.lef')
process('skywater-pdk-libs-sky130_fd_io', 'sky130_fd_io.lef')
process('skywater-pdk-libs-sky130_fd_pr', 'sky130_fd_pr.lef')

os.system('cp skywater-pdk-libs-sky130_fd_sc_hd/tech/*.tlef .')
os.system('cp skywater-pdk-libs-sky130_fd_sc_hdll/tech/*.tlef .')
os.system('cp skywater-pdk-libs-sky130_fd_sc_ms/tech/*.tlef .')
os.system('cp skywater-pdk-libs-sky130_fd_sc_ls/tech/*.tlef .')
os.system('cp skywater-pdk-libs-sky130_fd_sc_lp/tech/*.tlef .')
os.system('cp skywater-pdk-libs-sky130_fd_sc_hvl/tech/*.tlef .')
os.system('cp skywater-pdk-libs-sky130_fd_io/tech/*.tlef .')
os.system('cp skywater-pdk-libs-sky130_fd_pr/tech/*.tlef .')
