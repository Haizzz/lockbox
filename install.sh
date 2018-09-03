# install requirements
virtualenv env -p python3
source env/bin/activate
pip install -r requirements.txt
# build the executable
pyinstaller src/lockbox.py -F
# move executable outside and remove repo folder
cp dist/lockbox ../
cd ../
rm -rf lockbox_repo