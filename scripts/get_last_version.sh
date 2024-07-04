#!/bin/bash

tags=$(docker images --format \
"{{.Tag}}"  \
EremeevVV/cashback_memory);
IFS=$"\n" read -rd "" -a array <<<$tags
last_version=$(echo "${array[*]}" | sort -nr | head -n1)
echo $last_version