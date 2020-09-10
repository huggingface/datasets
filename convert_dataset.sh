#!/usr/bin/env bash

pathToFile=${1}
manual_dir=${2}

curPath=$(pwd)

if [ ! -f "${pathToFile}" ]; then
	echo "${pathToFile} does not exist"
	exit
fi

tfdsFolder=$(python -c "print('/'.join(\"${pathToFile}\".split('/')[:-1]))")
datasetName=$(python -c "print(\"${pathToFile}\".split('/')[-1].split('.')[0])")

# Step 0

# Uncomment if you want to clean your cache
#echo "### STEP 0 ### Clean your cache..."
#rm -rf "${curPath}/src/datasets/datasets/*"
#rm -rf "~/.cache/huggingface/datasets/*"

# Step 1

pathToFolder="datasets/${datasetName}"

echo ""
echo ""
if [ -f "${pathToFolder}/${datasetName}.py" ]; then
	echo "### STEP 1 ### ${datasetName} is already converted. To convert it again remove ${pathToFolder}/${datasetName}."
else
	echo "### STEP 1 ### Converting ${datasetName} dataset ..."
	eval "python datasets-cli convert --tfds_path ${pathToFile} --datasets_directory datasets/"
fi

if [ -f "${pathToFolder}/${datasetName}.py" ]; then
	echo "${datasetName}.py found in ${pathToFolder}"
else
	echo "${pathToFolder} must have a ${datasetName}.py, but was not found. Conversion error. Check conversion manually."
	exit
fi

echo "Conversion succesful!"

# STEP 2

echo ""
echo ""
if [ -f "${pathToFolder}/dataset_infos.json" ]; then
	echo "### STEP 2 ### Dataset infos file is already created. To create it again remove ${pathToFolder}/dataset_infos.json ..."
else
	echo "### STEP 2 ### Create infos ..."
	if [ -z "${manual_dir}" ]; then
		eval "python datasets-cli test ${pathToFolder} --save_infos --all_configs"
	else
		eval "python datasets-cli test ${pathToFolder} --data_dir ${manual_dir} --save_infos --all_configs"
	fi
fi

if [ -f "${pathToFolder}/dataset_infos.json" ]; then
	echo "dataset_infos.json found in ${pathToFolder}."
else
	echo "dataset_infos.json not found in ${pathToFolder}. Add dataset infos manually."
	exit
fi

# rm lock file
rm ${pathToFolder}/*.lock

echo "Dataset infos creation succesful!"

echo ""
echo ""
echo "### STEP 3 ### Make style ..."
eval "make style"

echo ""
echo ""

cd ${pathToFolder}
name=${datasetName}
builderName=$(python -c "import stringcase; print(stringcase.pascalcase(\"${name}\"));")

configNames=$(python -c "from ${name} import ${builderName}; [print(x.name) for x in ${builderName}.BUILDER_CONFIGS];")

versions=$(python -c "from ${name} import ${builderName}; [print(str(x.version.major) + '.' + str(x.version.minor) + '.' + str(x.version.patch)) for x in ${builderName}.BUILDER_CONFIGS];")

mainVersion=$(python -c "from ${name} import ${builderName}; print(str(${builderName}.VERSION.major) + '.' + str(${builderName}.VERSION.minor) + '.' + str(${builderName}.VERSION.patch));")

if [ ! -z "${versions}" ]; then
	versionArray=(`echo $versions`)
else
	versionArray=(`echo $mainVersion`)
fi

for version in "${versionArray[@]}"; do
	echo "Found version name ${version}"
	firstVersion=${versionArray[0]}
done

configArray=(`echo $configNames`)
for config in "${configArray[@]}"; do
	echo "Found config name ${config}"
	firstConfig=${configArray[0]}
done

if [ -d "./dummy" ]; then
	echo "### STEP 4 & 5 ### dummy folder is already created. To rerun the command, delete ${pathToFolder}/dummy"
	cd ${curPath}
else
	echo "### STEP 4 ### Create dummy folder structure..."

	if [ -z "${configNames}" ]; then
		echo "${datasetName} has no configs. Create dummy data without config folder ... "

		mkdir -p ${curPath}/${pathToFolder}/dummy/${firstVersion}/
		echo "Created ${curPath}/${pathToFolder}/dummy/${firstVersion} ..."
	else
		echo "${datasetName} has config. Create dummy data with config folder ... "
		for ((i=0;i<${#configArray[@]};++i)); do
			config=${configArray[i]}
			version=${versionArray[i]}
			mkdir -p ${curPath}/${pathToFolder}/dummy/${config}/${version}/
			echo "Created ${curPath}/${pathToFolder}/dummy/${config}/${version} ..."
		done
	fi


	cd ${curPath}

	echo ""
	echo ""
	echo "### STEP 5 ### Create dummy data from ${fakeDataFolder}"

	echo "${tfdsFolder}"
	fakeDataFolder=$(readlink -m ${tfdsFolder}/../testing/test_data/fake_examples/${datasetName})

	if [ -d "${fakeDataFolder}" ]; then
		echo "fake data folder found in ${fakeDataFolder}"
	else
		echo "fake data folder not found. ${fakeDataFolder} does not exist. Create dummy data manually."
		exit
	fi

	echo "Zipping and copying data from ${fakeDataFolder}..."
	cd "${fakeDataFolder}"
	dirFilesAndFolders=$(ls)
	mkdir dummy_data
	for dir in "${dirFilesAndFolders}"; do
		echo "Adding ${dir} to dummy_data zip dir"
		cp -r ${dir} dummy_data/
	done
	eval "zip -r dummy_data.zip dummy_data"
	rm -r dummy_data

	# Copy zipped data to correct file
	if [ -z "${configNames}" ]; then
		eval "mv dummy_data.zip ${curPath}/${pathToFolder}/dummy/${version}/dummy_data.zip"
	else
		if [ "${#configArray[@]}" -gt 1 ]; then
			echo "Dataset has multiple configs. Copy zip data to first config: ${firstConfig}..."
			echo "IMPORTANT: Fix zipped dummy data manually!"
			eval "mv dummy_data.zip ${curPath}/${pathToFolder}/dummy/${firstConfig}/${version}/dummy_data.zip"
		else
			echo "Copy zip data to first config: ${firstConfig}..."
			eval "mv dummy_data.zip ${curPath}/${pathToFolder}/dummy/${firstConfig}/${version}/dummy_data.zip"
		fi
	fi
	cd "${curPath}"
fi

# rm pycache
rm -rf ${pathToFolder}/__pycache__

if [ -f ${curPath}/${pathToFolder}/dummy/${firstVersion}/dummy_data.zip ] || [ -f ${curPath}/${pathToFolder}/dummy/${firstConfig}/${firstVersion}/dummy_data.zip ] ; then
	echo ""
	echo ""
	echo "Conversion succesful!"
	echo ""
	echo ""
	echo "Check that the following two commands work:"
	echo "RUN_SLOW=1 pytest tests/test_dataset_common.py::DatasetTest::test_load_real_dataset_local_${datasetName}"
echo "RUN_SLOW=1 pytest tests/test_dataset_common.py::DatasetTest::test_load_dataset_all_configs_local_${datasetName}"
echo "pytest tests/test_dataset_common.py::DatasetTest::test_load_dataset_local_${datasetName}"
fi
