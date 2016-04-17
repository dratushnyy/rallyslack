#! /bin/bash
openssl ecparam -genkey -name prime256v1 -out rallyslack.key
openssl req -new -key rallyslack.key -out rallyslack.pem
openssl req -x509 -days 365 -key rallyslack.key -in rallyslack.pem -out rallyslack.crt