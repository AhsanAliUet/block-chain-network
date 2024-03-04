set -e # Exit immediately is some error occurs

## install dependencies
sudo apt-get update -y
sudo apt-get upgrade -y
sudo apt-get install curl jq make git build-essential -y

## ==================== Install go ====================

if [ ! $(which go) ]
then
    echo ""
    echo "Installing Go..."
    echo ""
    rm -rf go1.22.0.linux-amd64.tar.gz
    wget https://dl.google.com/go/go1.22.0.linux-amd64.tar.gz
    tar -xzf go1.22.0.linux-amd64.tar.gz
    sudo rm -rf /usr/local/go
    sudo mv go/ /usr/local/
    rm -rf go1.22.0.linux-amd64.tar.gz
    echo "export PATH=/usr/local/go/bin:\$PATH" >> ~/.bashrc
    echo ""
    eval "$(cat ~/.bashrc | tail -n +10)"  # source ~/.bashrc
    echo ""
    echo "Succesfully installed Go in $(which go)"
    echo ""
else
    echo ""
    echo "Go is already present in $(which go)"
    echo ""
fi
# ==================== Install geth ====================

if [ ! $(which geth) ]
then
    echo ""
    echo "Installing Quorum..."
    echo ""

    git clone https://github.com/Consensys/quorum.git
    cd quorum && make all
    cd ..
    mkdir quorum_bins
    cp $PWD/quorum/build/bin/* $PWD/quorum_bins
    rm -rf quorum
    sudo mv quorum_bins /usr/local/
    echo "export PATH=/usr/local/quorum_bins:\$PATH" >> ~/.bashrc
    echo ""
    eval "$(cat ~/.bashrc | tail -n +10)"  # source ~/.bashrc
    echo ""
    echo "Succesfully installed Quorum in $(which geth)"
    echo ""
else
    echo ""
    echo "geth is already present in $(which geth)"
    echo ""
fi
## ==================== Install istanbul-tools ====================

if [ ! $(which istanbul) ]
then
    echo ""
    echo "Installing istanbul-tools..."
    echo ""

    git clone https://github.com/ConsenSys/istanbul-tools.git
    cd istanbul-tools && make
    cd ..
    mkdir istanbul_tools_bins
    cp $PWD/istanbul-tools/build/bin/* $PWD/istanbul_tools_bins
    rm -rf istanbul-tools
    sudo mv istanbul_tools_bins /usr/local/
    echo "export PATH=/usr/local/istanbul_tools_bins:\$PATH" >> ~/.bashrc
    echo ""
    eval "$(cat ~/.bashrc | tail -n +10)"  # source ~/.bashrc
    echo ""
    echo "Succesfully istanbul-tools in $(which istanbul)"
    echo ""
else
    echo ""
    echo "istanbul is already present in $(which istanbul)"
    echo ""
fi

eval "$(cat ~/.bashrc | tail -n +10)"  # source ~/.bashrc
source ~/.bashrc

echo ""
echo "You are all set. Installed all the tools!"
echo ""

## ==================== end ====================