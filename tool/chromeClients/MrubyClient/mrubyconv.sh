export PATH=/usr/local/bin:/usr/bin

echo start >> $3


$1 $2 2>> $3

var=`tail -1 $3`
if [ "$var" == "start" ]
	then
	echo mrb succeeded. >> $3
else
	echo mrb failure. >> $3
fi


