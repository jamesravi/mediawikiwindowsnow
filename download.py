# Copyright (C) 2022 James Ravindran
# SPDX-License-Identifier: GPL-3.0-or-later

import zipfile
import os
from pathlib import Path
import glob
import shutil
from tqdm import tqdm
import requests

# Change settings here
# WARNING: These programs would be probably get out of date in the future, and some paths might need correcting if they are updated
BASE = "site"
APACHE_URL = "https://www.apachelounge.com/download/VS16/binaries/httpd-2.4.54-win64-VS16.zip"
APACHE_ZIP_FOLDERNAME = "Apache24"
PHP_URL = "https://windows.php.net/downloads/releases/php-7.4.30-Win32-vc15-x64.zip"
MEDIAWIKI_URL = "https://releases.wikimedia.org/mediawiki/1.38/mediawiki-1.38.2.zip"
MEDIAWIKI_ZIP_FOLDERNAME = "mediawiki-1.38.2"

###

# https://stackoverflow.com/a/39217788
def download_file(url, dst_filename):
    Path(dst_filename).parent.mkdir(parents=True, exist_ok=True)
    with requests.get(url, stream=True, headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36"}) as r:
        with open(dst_filename, 'wb') as f:
            shutil.copyfileobj(r.raw, f)
            
def extract_folder_from_zip(zipfilename, dst_folder, foldername=None):
    with zipfile.ZipFile(zipfilename) as archive:
        if foldername != None:
            for filename in tqdm(archive.namelist()):
                if filename.startswith(f"{foldername}/"):
                    archive.extract(filename, "temp")
        else:
            foldername = "temproot"
            archive.extractall("temp\\"+foldername)
            
    Path(dst_folder).parent.mkdir(parents=True, exist_ok=True)
    os.rename(f"temp\\{foldername}", dst_folder)
    
def download_zip(url, print_name):
    filename = "temp\\"+url.split("/")[-1]
    if os.path.isfile(filename):
        print(f"Already downloaded {print_name} zip")
    else:
        print(f"No {print_name} zip found, downloading...")
        download_file(url, filename)

def perform_zip_extraction(url, dst_folder, foldername, print_name):
    if not os.path.isdir(dst_folder):
        print(f"No {print_name} folder found")
        download_zip(url, print_name)
        print(f"Extracting {print_name} from zip")
        extract_folder_from_zip(f"temp\\{url.split('/')[-1]}", dst_folder, foldername)
    else:
        print(f"{print_name} folder already exists")

def fixapache():
    dir_path = os.path.dirname(os.path.realpath(__file__))
    apacheconf = BASE + r"\apache\conf\httpd.conf"
    
    lines = []
    with open(apacheconf) as dafile:
        for line in dafile:
            line = line.strip()
            if line.startswith("Define SRVROOT "):
                print("Setting Apache SRVROOT")
                line = "Define SRVROOT " + dir_path + f"\\{BASE}\\apache"
            if not any(line.startswith(start) for start in ["PHPIniDir ", "LoadModule php7_module ", "AddType application/x-httpd-php "]):
                lines.append(line)

    print("Adding lines for Apache to load PHP")
    lines = "\n".join(lines).rstrip().split("\n")
    lines.append("")
    lines.append(f'PHPIniDir "{dir_path}\\{BASE}\\php"')
    lines.append(f'LoadModule php7_module "{dir_path}\\{BASE}\\php\\php7apache2_4.dll"')
    lines.append("AddType application/x-httpd-php .php")

    with open(apacheconf, "w") as dafile:
        dafile.write("\n".join(lines))

def fixphp():
    php_dir = BASE + "\\php"
    php_ini_filename = f"{php_dir}\\php.ini"
    
    if not os.path.isfile(php_ini_filename):
        os.rename(php_ini_filename+"-production", php_ini_filename)
    
    exts = [";extension=fileinfo", ";extension=intl", ";extension=mbstring", ";extension=pdo_sqlite", ";extension=sqlite3"]
    
    lines = []
    extraline = f"extension_dir = {php_dir}\\ext"
    print("Setting lines to load PHP extensions")
    with open(php_ini_filename) as dafile:
        for line in dafile:
            line = line.strip()
            if line in exts:
                line = line[1:]
            if extraline == line:
                extraline = ""
            lines.append(line)
            
    if extraline != "":
        print("Setting PHP extension_dir")
        lines.extend(["", extraline])
    else:
        print("PHP extension_dir already set")
            
    with open(php_ini_filename, "w") as dafile:
        dafile.write("\n".join(lines))
        
    print("Copying dlls for intl extension")
    for filename in glob.glob(php_dir+"\\*.dll"):
        if filename.startswith(php_dir+"\\icu"):
            shutil.copy(filename, BASE+"\\apache\\bin")
    
    shutil.copy(php_dir+"\\libsqlite3.dll", BASE+"\\apache\\bin")

# Apache
perform_zip_extraction(APACHE_URL, BASE+"\\apache", APACHE_ZIP_FOLDERNAME, "Apache")

# PHP
perform_zip_extraction(PHP_URL, BASE+"\\php", None, "PHP")

# MediaWiki (must be run after Apache extraction)
perform_zip_extraction(MEDIAWIKI_URL, BASE+"\\apache\\htdocs\\mediawiki", MEDIAWIKI_ZIP_FOLDERNAME, "MediaWiki")

indexhtml = BASE+"\\apache\\htdocs\\index.html"
if os.path.isfile(indexhtml):
    print("Removing default Apache index.html")
    os.remove(indexhtml)

fixapache()
fixphp()

print("Done!")