# lockbox
Drop and lock(encrypt) a folder

## Prerequisites
Python 3.6 and above

## Getting started
Lockbox uses [pyinstaller](https://www.pyinstaller.org/) to create an executable from the python code for different platforms, to download and build the executable, run:
```bash
# clone repo
git clone https://github.com/Haizzz/lockbox.git lockbox_repo
cd lockbox_repo
bash install.sh
```

The executable is now built. Copy this file into your folder and double click to set a password and get started

## Usage
![Usage gif](https://github.com/Haizzz/lockbox/blob/master/media/usage.gif?raw=True)

## Notes
- The extension `.locked` is used to tell lockbox is a file is already encrypted
- Files that can't be written to due to insufficient permission **will be skipped**

