#!/bin/sh

set -xe

cd $(dirname $0)/../data


pipenv run python3 ../src/tokenize_file.py --add-tag --input dev/dev.tgt \
	--output dev/dev.token.tgt &
p1="$!"

pipenv run python3 ../src/tokenize_file.py --input dev/dev.src \
	--output dev/dev.token.src &
p2="$!"

pipenv run python3 ../src/tokenize_file.py --has-tag --input train/x/train.tgt \
	--output train/train.tgt &
p3="$1"

pipenv run python3 ../src/tokenize_file.py --input train/x/train.src \
	--output train/train.src &
p4="$!"

wait $p1
wait $p2
wait $p3
wait $p4
