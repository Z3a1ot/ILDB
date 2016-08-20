#!/usr/bin/env bash


lockfile=$1

(set -o noclobber; echo "$$" > "$lockfile") 2> /dev/null
while [ $? != 0 ]; do
(set -o noclobber; echo "$$" > "$lockfile") 2> /dev/null
done


trap 'rm -f "$lockfile"; exit $?' INT TERM EXIT

cat $2 2> /dev/null

rm -f "$lockfile"
trap - INT TERM EXIT