#!/usr/bin/env bash

# Each dummy_data.zip file contains the json files of all the languages
# This script removes the unnecessary json files to reduce the size of each dummy_data.zip

cd $(dirname $0) # go to the directory of this script

# Get the json files from some language
unzip ./xquad.ar/1.0.0/dummy_data.zip

for json_file in $(ls ./dummy_data); do
    config_name=$(basename ${json_file} .json)
    rm ./${config_name}/1.0.0/dummy_data.zip
    zip -m ./${config_name}/1.0.0/dummy_data.zip ./dummy_data/${json_file} # zip json file and delete it
done

rm -r dummy_data
