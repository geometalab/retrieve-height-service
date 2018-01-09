#!/bin/bash
# wget -L --random-wait --timestamping --load-cookies ~/.cookies --save-cookies ~/.cookies -i data_list_2018-01-09.txt
# only execute this once, therefore commented

# normal execution
# wget --random-wait -i data_list.txt --timestamping
# execute in parallel, especially when havin a fast internet connection quite usefull
# cat ../data_list.txt | parallel --gnu "wget --random-wait --timestamping {}"

# unzip hgts
unzip *.zip

# build worldfile
gdalbuildvrt world.vrt *.hgt

# "healthcheck" of worldfile
gdalinfo -mm world.vrt
