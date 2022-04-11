cd docs

function deploy_doc(){
	echo "Creating doc at commit $1 and pushing to folder $2"
	git checkout $1
	if [ ! -z "$2" ]
	then
		if [ "$2" == "master" ]; then
		    echo "Pushing master"
			make clean && make html && scp -r -oStrictHostKeyChecking=no _build/html/* $doc:$dir/$2/
			cp -r _build/html/_static .
		elif ssh -oStrictHostKeyChecking=no $doc "[ -d $dir/$2 ]"; then
			echo "Directory" $2 "already exists"
			scp -r -oStrictHostKeyChecking=no _static/* $doc:$dir/$2/_static/
		else
			echo "Pushing version" $2
			make clean && make html
			rm -rf _build/html/_static
			cp -r _static _build/html
			scp -r -oStrictHostKeyChecking=no _build/html $doc:$dir/$2
		fi
	else
		echo "Pushing stable"
		make clean && make html
		rm -rf _build/html/_static
		cp -r _static _build/html
		scp -r -oStrictHostKeyChecking=no _build/html/* $doc:$dir
	fi
}

# You can find the commit for each tag on https://github.com/huggingface/datasets/tags
# Deploys the master documentation on huggingface.co/docs/datasets/master
deploy_doc "master" master

# Example of how to deploy a doc on a certain commit (the commit doesn't have to be on the master branch).
# The following commit would live on huggingface.co/docs/datasets/v1.0.0
deploy_doc "faf3d79" v1.18.4
deploy_doc "c6bc52a" v1.18.3
deploy_doc "ba00b25" v1.18.2
deploy_doc "218e496" v1.18.1
deploy_doc "c0aea8d" v1.18.0
deploy_doc "dff6c92" v1.17.0
deploy_doc "acca8f4" v1.16.1
deploy_doc "d50f5f9" v1.16.0
deploy_doc "0181006" v1.15.1
deploy_doc "dcaa3c0" v1.15.0
deploy_doc "ec82422" v1.14.0
deploy_doc "10dc68c" v1.13.3
deploy_doc "e82164f" v1.13.2
deploy_doc "2ed762b" v1.13.1
deploy_doc "38ec259" v1.13.0
deploy_doc "2c1fc9c" v1.12.1
deploy_doc "c65dccc" v1.12.0
deploy_doc "ea7f0b8" v1.11.0
deploy_doc "cea1a29" v1.10.2
deploy_doc "6b7b227" v1.10.1
deploy_doc "3aabafb" v1.10.0
deploy_doc "5bc064d" v1.9.0
deploy_doc "bcf0543" v1.8.0
deploy_doc "448c177" v1.7.0
deploy_doc "b0d7ae1" v1.6.2
deploy_doc "e8fc41f" v1.6.1
deploy_doc "40bb9e6" v1.6.0
deploy_doc "f256b77" v1.5.0
deploy_doc "ca41320" v1.4.1
deploy_doc "f42658e" v1.4.0
deploy_doc "ef633da" v1.3.0
deploy_doc "a59580b" v1.2.1
deploy_doc "dae6880" v1.2.0
deploy_doc "000b584" v1.1.3
deploy_doc "2256521" v1.1.2
deploy_doc "8029965" v1.1.1
deploy_doc "fe52b67" v1.1.0
deploy_doc "af7cd94" v1.0.2
deploy_doc "7c9d2b5" v1.0.1
deploy_doc "322ba0e" v1.0.0
deploy_doc "99e0ee6" v0.3.0
deploy_doc "21e8091" v0.4.0

# Replace this by the latest stable commit. It is recommended to pin on a version release rather than master.
deploy_doc "master"
