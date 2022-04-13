#!/bin/bash

CUR=`pwd`
STATIC_DIR=/var/www/sample_flask/static


rsync -a --delete --stats ./app/static/ $STATIC_DIR 
chown -R www-data:www-data $STATIC_DIR
ls -l $STATIC_DIR

cd $CUR
