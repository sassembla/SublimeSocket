export PATH=/usr/local/bin:/usr/bin

#$1 = .rb files array
#$2 = logFilePath

echo start >> $2


/Users/sassembla/test/mruby/bin/mruby $1 1>> $2

var=`tail -1 $2`
if [ "$var" == "start" ]
	then
	echo mruby compile succeeded. >> $2
else
	echo mruby compile failure. >> $2	
fi


