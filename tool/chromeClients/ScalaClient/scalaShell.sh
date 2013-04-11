export PATH=/usr/local/bin:/usr/bin

#$1 = .ts files array
#$2 = logFilePath

echo start >> $1

#tsc includes "node" call
/usr/local/bin/gradle build 2>> $1

var=`tail $1`
echo $var

# if [ "$var" == "start" ]
# 	then
# 	echo typescript compile succeeded. >> $1
# else
# 	echo typescript compile failure. >> $1
# fi


