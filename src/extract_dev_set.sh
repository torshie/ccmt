#!/bin/sh

set -xe

cd $(dirname $0)/../data



tar xfvz dev.tgz \
	dev/newsdev2017-enzh-src.en.sgm \
	dev/newstest2017-zhen-src.zh.sgm

../src/xml_to_text.sh < dev/newsdev2017-enzh-src.en.sgm > dev/dev.src
../src/xml_to_text.sh < dev/newsdev2017-enzh-ref.zh.sgm > dev/dev.tgt
