# Copyright (C) 2022 James Ravindran
# SPDX-License-Identifier: GPL-3.0-or-later

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
