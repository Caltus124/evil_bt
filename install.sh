

#!/bin/bash

clear
GREEN="\e[32m"
RED="\e[31m"
ENDCOLOR="\e[0m"


if [ $(id -u) -ne 0 ]
then
        echo -e "${RED}The installation must be run as root !${ENDCOLOR}" 
        exit 1
else
        if [ -f "/opt/evil_bt/app.py" ]
        then
                echo "/usr/bin/python3 /opt/evil_bt/app.py" > /bin/evilbt
                chmod +x /bin/evilbt
                echo "cd /opt/evil_bt && hciconfig hci0 up && python3 -m flask run " > /bin/evilbt
                pip install -r requirements.txt
                echo -e "${GREEN}Successful installation, thanks for choosing Evil_BT !${ENDCOLOR}"
                rm -rf "/opt/evil_bt/install.sh"
        else
                echo -e "${RED}The installation file does not exist, please save the project in '/opt' !${ENDCOLOR}" 
        fi
fi
