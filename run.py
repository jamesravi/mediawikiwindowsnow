"""
mediawikiwindowsnow - simple scripts to download and do the bare minimum to configure MediaWiki, PHP and Apache to run on Windows
Copyright (C) 2022 James Ravindran

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""

import subprocess
import sys
import webbrowser
import os

# Change settings here
BASE = "site"

###

cmd = BASE + r"\apache\bin\httpd.exe"
retcode = 0

if os.path.isfile(cmd):
    webbrowser.open("http://localhost/mediawiki/index.php")

    try:
        retcode = subprocess.call([cmd])
    except KeyboardInterrupt:
        pass

    sys.exit(retcode)
else:
    print("No httpd.exe found, download and setup Apache and others using download.py")
