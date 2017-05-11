#!/bin/bash
args=("$@")
cd ..
bench new-site ${args[0]} --mariadb-root-username root --mariadb-root-password 1 --admin-password ${args[2]} --install-app erpnext
#whoami
#bench --site ${args[0]} set-admin-password ${args[2]}
bench --site ${args[0]} install-app erpstyle

bench set-nginx-port ${args[0]} ${args[3]}

bench setup nginx --y

sudo service nginx reload


bench use ${args[0]}
#./script site11 123456 123456 9090
