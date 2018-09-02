# lockbox
Drop and lock(encrypt) a folder

## Getting started
Lockbox uses [pyinstaller](https://www.pyinstaller.org/) to create an executable from the python code for different platforms, to download and build the executable, run:
```bash
# clone repo
git clone https://github.com/Haizzz/lockbox.git lockbox_repo
cd lockbox_repo
# install requirements
virtualenv env -p python3
source env/bin/activate
pip install -r requirements.txt
# build the executable
pyinstaller lockbox.py -F
# move executable outside and remove repo folder
cp dist/lockbox ../
cd ../
rm -rf lockbox_repo
```

The executable is now inside the `dist` folder. Copy this file into your folder and double click to set a password and get started

## Notes
- The extension `.locked` is used to tell lockbox is a file is already encrypted
- Files that can't be written to due to insufficient permission **will be skipped**

