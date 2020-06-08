STAGE=$1
SCRIPT_NUM=2
# this snippet can be used in other scripts to check if already deployed
echo "Checking if system is already deployed"
cd $PWD/deployment_scripts/common || exit
python check_version_not_run.py $STAGE $SCRIPT_NUM
if [ $? = 1 ]; then
    echo "Script already run. Exiting..."
    exit 1
fi
cd ../.. || exit

echo "Provisioning S3 Upload bucket resources"
cd $PWD/deployment_scripts/2_deploy_upload_bucket || exit
python provision_upload_bucket.py $STAGE

if [ $? = 0 ]; then
    echo "Successfully provisioned"
else
    echo "Provisioning failed"
    exit 1
fi

cd ../.. || exit

echo "Updating deployment version"
cd $PWD/deployment_scripts/common || exit
python update_version.py $STAGE $SCRIPT_NUM

if [ $? = 0 ]; then
    echo "Version successfully added to deployment table"
else
    echo "Version already exists or deployment table doesn't exist. Exiting..."
    exit 1
fi