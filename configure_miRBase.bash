# Script for downloading and preparing necessary miRBase files
miRBase_version="22.1"
PYTHON="python3"

mkdir -p miRBase
cd miRBase

# Download files
wget "ftp://mirbase.org/pub/mirbase/${miRBase_version}/hairpin.fa.zip"
wget "ftp://mirbase.org/pub/mirbase/${miRBase_version}/mature.fa.zip"
wget "ftp://mirbase.org/pub/mirbase/${miRBase_version}/miRNA.str.zip"

# Unzip them
unzip hairpin.fa.zip
unzip mature.fa.zip
unzip miRNA.str.zip
rm -f *.zip

# Now process them for further use
cd ..
${PYTHON} prepare_miRBase.py
