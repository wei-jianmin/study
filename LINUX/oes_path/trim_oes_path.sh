#!/bin/bash
#refer ./oes_path.sh create tmp.sh and then replace /oes_path.sh with attr i
if [ ! `whoami` = root ]; then
    echo "need root authority"
    exit
fi
echo '#!/bin/bash' > oes_path2.sh
sed "/^#/d;/^$/d" oes_path.sh >> oes_path2.sh
if [ -e /oes_path.sh ]; then
	chattr -i /oes_path.sh
fi
mv oes_path2.sh /oes_path.sh
chattr +i /oes_path.sh
