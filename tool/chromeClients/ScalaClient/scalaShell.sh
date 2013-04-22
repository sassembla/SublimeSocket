export PATH=/usr/local/bin:/usr/bin:/bin

#$1 = "build.gradle includes" filePath
#$2 = logFilePath

echo start >> $2

echo $1 >> $2

cd $1
#gradle includes "bash" call
gradle build -i >> $2
