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

# You can find the commit for each tag on https://github.com/huggingface/nlp/tags
# Deploys the master documentation on huggingface.co/nlp/master
deploy_doc "master" master

# Example of how to deploy a doc on a certain commit (the commit doesn't have to be on the master branch).
# The following commit would live on huggingface.co/nlp/v1.0.0
#deploy_doc "b33a385" v1.0.0
deploy_doc "99e0ee6" v0.3.0
deploy_doc "21e8091" v0.4.0

# Replace this by the latest stable commit. It is recommended to pin on a version release rather than master.
deploy_doc "master"
