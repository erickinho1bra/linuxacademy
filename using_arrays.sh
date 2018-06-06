#!/bin/bash

MYARRAY=(Brazil Germany France Spain Argentina)
COUNT=0

for i in ${MYARRAY[@]}; do
	echo "Countries in the World Cup 2018: ${MYARRAY[COUNT]}"
	COUNT=`expr "$COUNT" + 1`
done
echo all done!

