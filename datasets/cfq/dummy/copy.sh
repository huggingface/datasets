#!/usr/bin/env bash

curPath=$(pwd)

for dir in $(ls); do
 if [ -d ${curPath}/${dir} ]; then
	 eval "unzip dummy_data_copy.zip"
	 eval "mv dummy_data/cfq/splits/data.json dummy_data/cfq/splits/${dir}.json"
	 eval "zip -r dummy_data.zip dummy_data"
	 eval "cp dummy_data.zip ${curPath}/${dir}/1.0.1/dummy_data.zip"
	 eval "rm dummy_data.zip"
	 eval "rm -r dummy_data"
 fi
done
