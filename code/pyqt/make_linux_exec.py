#!/usr/bin/env python
#
# 	make_linux_exec.py
#
#   Executable builder for the Football Match Result Database (FMRD)
#
#   Copyright (C) 2010-2011, Howard Hamilton
#
#   This program is free software: you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation, either version 3 of the License, or
#   (at your option) any later version.
#
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public License
#   along with this program.  If not, see <http://www.gnu.org/licenses/>.

import os
import subprocess

# PyInstaller path and scripts
PyInstaller = "/usr/local/src/pyinstaller-1.5/"
MakeSpec = "Makespec.py"
Build = "Build.py"

# Name of main GUI app file
MainFile = "fmrd_main.pyw"

# Directories
ExecDir = "../../"
SourcePath = ".:FmrdAdmin/:FmrdLib/:FmrdMain/"

# Executable filename fragments
ExecPrefix = "fmrd-desktop-"
VERSIONTAG = "v1.1.0"
PLATFORM = "-linux"

# Form commands
specString = PyInstaller+MakeSpec+" --upx --name="+ExecPrefix+VERSIONTAG+PLATFORM+" --out="+ExecDir+" --path="+SourcePath+" --onefile "+MainFile
buildString = PyInstaller+Build+" "+ExecDir+ExecPrefix+VERSIONTAG+PLATFORM+".spec"

# Execute commands
subprocess.call(specString,shell=True)
subprocess.call(buildString,shell=True)

