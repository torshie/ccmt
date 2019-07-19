#!/bin/sh

set -xe

cd $(dirname $0)/../data


pipenv run python3 ../src/tokenize_file.py --add-tag --input dev/dev.tgt \
	--output dev/dev.token.tgt

pipenv run python3 ../src/tokenize_file.py --input dev/dev.src \
	--output dev/dev.token.src

pipenv run python3 ../src/tokenize_file.py --has-tag --input train/train.tgt \
	--output train/train.token.tgt

pipenv run python3 ../src/tokenize_file.py --input train/train.src \
	--output train/train.token.src
