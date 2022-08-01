# mediawikiwindowsnow
Simple scripts to download and do the bare minimum to configure MediaWiki, PHP and Apache to run on Windows.

## ⚠️ Warning ⚠️
* I'd recommended this only for a personal/development wiki. Security isn't considered at all, so it shouldn't be used in production.
* The script is hardcoded to the latest compatible versions of MediaWiki, PHP and Apache as of July 2022. It's likely they will be outdated in the future, and that some paths might need correcting if they are updated.
* It's likely possible more extensions etc. will need to be enabled, which I will probably uncover once I setup MediaWiki. It's likely the script will get more complex as I add extensions used on Wikipedia.

## How to use
1. First, you need to install Python 3 and some dependencies:  
`pip install requests tqdm`
3. Then, run `download.py` to download, extract and configure MediaWiki, Apache and PHP (this may need to be rerun if you move the folder where everything is located, and you can save time by copying the temp folder containing all the zips to avoid redownloading everything).
4. Finally, `run.py` will start Apache, and your browser should open MediaWiki automatically, so you can start setting up your portable wiki!

## License
[GPLv3 or later](LICENSE.txt)