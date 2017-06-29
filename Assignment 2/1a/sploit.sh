#!/bin/bash

ATTACK_USERNAME="alice"
ATTACK_PASSWORD="passw0rd"

if [ $# -ne 2 ]; then
	PREFIX="ugster21.student.cs.uwaterloo.ca/sdsuo"
else
	IP=$1
	PORT=$2
	PREFIX=$IP:$PORT
fi

POST_PAGE=http://$PREFIX/post.php
HOME_PAGE=http://$PREFIX/index.php
echo "=====[Setup]====="
echo "Using Login Page at $POST_PAGE"
echo "Using Home Page at $HOME_PAGE"

echo "Using attack username $ATTACK_USERNAME"
echo "Using attack password $ATTACK_PASSWORD"

echo "=====[Login]====="
echo "Logging in with POST request"
curl \
-X POST \
-c "cookie.txt" \
-F "form=login" \
-F "submit=Login" \
-F "uername=$ATTACK_USERNAME" \
-F "password=$ATTACK_PASSWORD" \
$POST_PAGE

echo "=====[Index]====="
echo "Showing index page with GET request"
curl \
-b cookie.txt \
$HOME_PAGE