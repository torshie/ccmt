#!/bin/sh

set -xe

cd $(dirname $0)/../data

pipenv run fairseq-preprocess --source-lang src --target-lang tgt \
	--trainpref train/train.token --validpref dev/dev.token \
	--thresholdtgt 5 --thresholdsrc 5 --destdir data-bin \
	"$@"
