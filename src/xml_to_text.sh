#!/bin/sh

set -xe

grep '<seg id=' \
	| sed -e 's/<seg id="[[:digit:]]*">//' -e 's@</seg>@@' \
	| /usr/bin/env python3 -c "
import html
import sys
for line in sys.stdin:
	print(html.unescape(line.strip()))
"
