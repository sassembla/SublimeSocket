export PATH=/usr/local/bin

#$1 = .ts files array
#$2 = logFilePath

echo start > $2

#tsc includes "node" call
/usr/local/bin/tsc $1 2>> $2
echo completed >> $2
