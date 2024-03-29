STAGE=test
CONFIG_FILE="./config.$STAGE.json"

if [ -f $CONFIG_FILE ];
then
    echo "starting installation of prerequisites"
else
    echo "$CONFIG_FILE not found. Please enter the name of one the stages you have prepared a config file for: "
    read -p "stage: " STAGE
    CONFIG_FILE="./config.$STAGE.json"

    if [ -f $CONFIG_FILE ];
    then
        echo "starting installation of prerequisites"
    else
        echo "$CONFIG_FILE not found."
        exit
    fi
fi

if [ ! -f $CONFIG_FILE ]; then
    echo "$FILE exist"
fi

cd ./services || exit

echo "Installing serverless"
npm install -g serverless

echo "Installing serverless plugins"
sls plugin install -n serverless-python-requirements --stage $STAGE
sls plugin install -n serverless-pseudo-parameters --stage $STAGE
sls plugin install -n serverless-prune-plugin --stage $STAGE

cd .. || exit
echo "Setting up virtualenv"
virtualenv -p python3.6 .
. ./bin/activate
pip install -r requirements-dev.txt

if [ $? = 0 ]; then
    echo "\n**************************\n"
    echo "Requirements installed successfully. Please run 'source bin/activate' to activate the virtual environment"
    echo "\n**************************\n"
else
    echo "\n**************************\n"
    echo "Installation of requirements failed"
    echo "\n**************************\n"
    exit 1
fi