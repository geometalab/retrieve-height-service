#!/bin/bash

echo "You need an user account to download data; Please create on in order to use this downloader at https://urs.earthdata.nasa.gov."

# wget --user=$USER --ask-password --continue -L --random-wait --timestamping --load-cookies ~/.cookies --save-cookies ~/.cookies -i data_list_2018-01-09.txt
# execute in parallel, especially when havin a fast internet connection
# cat ../data_list_2018-01-09.txt | parallel --gnu "wget --user=$USER --ask-password --continue -L --random-wait --timestamping --load-cookies ~/.cookies --save-cookies ~/.cookies {}"

echo ""
echo "
##############

wget --user=$USER --ask-password --continue -L --random-wait --timestamping --load-cookies ~/.cookies --save-cookies ~/.cookies -i data_list_2018-01-09.txt

**WARNING**: before continuing, check that 
`cat data_list_2018-01-09.txt |  wc -l` and `ls -l *.zip | wc -l` is the same.

ie. `cat data_list_2018-01-09.txt |  wc -l -eq ls -l *.zip | wc -l`

Next steps:

# unzip hgts
unzip *.zip

# build worldfile
gdalbuildvrt -a_srs EPSG:3857 world.vrt *.hgt

# healthcheck of worldfile
gdalinfo -mm world.vrt
"
