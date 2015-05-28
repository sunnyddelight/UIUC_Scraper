#!/bin/bash
if [ $# -ne 2 ]
then
  echo -e "\nUsage:\n $0 URL zip_filename\n"
  exit 0
fi
temp_dir=$(mktemp -d)
wget -r -l 1 -nd -nH -A pdf -P $temp_dir $1
zip $2 -j $temp_dir/*.pdf
rm -r $temp_dir
