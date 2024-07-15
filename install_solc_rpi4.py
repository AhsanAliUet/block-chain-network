import os

os.system("pip3 install py-solc-x --break-system-packages")
os.system("sudo apt update -y")

# check is cmake is there
try:
    os.system("sudo apt remove cmake -y")
except:
    pass

os.system("sudo apt-get install -y software-properties-common")
os.system("sudo apt install build-essential cmake libboost-all-dev -y")

import solcx

try:
    solcx.compile_solc('v0.8.26')
    print("\nSuccessfully installed solc")
except:
    print("\nError installing solcx!")
