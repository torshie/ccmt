#!/bin/sh

set -xe

cd $(dirname $0)

wget -c -O ../data/training-parallel-nc-v13.tgz \
	http://data.statmt.org/wmt18/translation-task/training-parallel-nc-v13.tgz
wget -c -O ../data/UNv1.0.en-zh.tar.gz \
	https://s3-us-west-2.amazonaws.com/twairball.wmt17.zh-en/UNv1.0.en-zh.tar.gz
wget -c -O ../data/ccmt.tar.gz \
	https://s3-us-west-2.amazonaws.com/twairball.wmt17.zh-en/cwmt.tgz
wget -c -O ../data/dev.tgz \
	http://data.statmt.org/wmt18/translation-task/dev.tgz
