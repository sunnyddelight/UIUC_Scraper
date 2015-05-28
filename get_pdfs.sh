#!/bin/bash
temp_dir=$(mktemp -d)
echo "hello"
wget -r -l 1 -nd -nH -A pdf -P $temp_dir $1
zip $2 -j $temp_dir/*.pdf
rm -r $temp_dir
