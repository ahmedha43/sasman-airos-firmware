#!/bin/sh
gid=`echo $REMOTE_USER | cut -d: -f3`
echo -e "Content-Type: text/plain;\r\n"
PATTERN='httpd.session'
if [ $gid != "0" ]; then
    grep $QUERY_STRING /tmp/system.cfg|grep $PATTERN
else
    grep $QUERY_STRING /tmp/system.cfg
fi
