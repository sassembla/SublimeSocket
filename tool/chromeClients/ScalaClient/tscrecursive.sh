# notyetwork

export PATH=/usr/local/bin:/usr/bin

#$1 = .ts files array
#$2 = logFilePath

echo start >> $2

#tsc includes "node" call
/usr/local/bin/tsc $1 2>> $2

var=`tail -1 $2`
if [ "$var" == "start" ]
	then
	echo typescript compile succeeded. >> $2
else
	echo typescript compile failure. >> $2	
fi


