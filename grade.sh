#!/bin/bash

cd /home/ftpuser/ftp

filename=$(ls -tr | tail -1)
id=${filename%.*}

#sudo python3 ${id}.py > /dev/null 1> ${id}.stdout
#sudo python3 ${id}.py > /dev/null 2> ${id}.stderr

sudo python3 ${id}.py 1> ${id}.stdout 2> ${id}.stderr

status=""

if [ -s "${id}.stdout" ]; then
   	diff answer.txt ${id}.stdout
	DIFF_RESULT=$?
	if [ ${DIFF_RESULT} -eq "0" ]; then
	    status="CORRECT"
	else
	    status="INCORRECT"
	fi
fi

if [ -s "${id}.stderr" ]; then
	status="ERROR"
fi

echo ${id}, ${status}

curl -X PATCH -H "content-type: application/json" -d '{"id": '$id', "status": "'"$status"'"}' "http://172.30.1.10:8000/submission"
