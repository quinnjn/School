#!/bin/sh

if [ $# -ne 1 ] ; then
	echo "Usage: $0 [workingdirectory]"
	echo "Where [workingdirectory] is the name of the directory where you have installed $0"
	exit 1
fi

if [ -d $1 ] ; then
	cd $1
else
	echo "Invalid working directory: $1"
	exit 1
fi

date=`date "+%b %d %H:%M"`

consumer_key=`grep "^consumer_key:" tweet.conf|awk -F: '{print $2}'`
consumer_secret=`grep "^consumer_key:" tweet.conf|awk -F: '{print $3}'`

grep "^$date|" tweet.txt|while read line
do
  echo "$line"|grep '|.*|.*|' >/dev/null
  if [ $? -eq 0 ] ; then
	echo "#Note from the $0 program:"
	echo "#You cannot have the pipe symbol (|) in a tweet, as we use this as a field separator." >>tweet.txt
	date=`echo $line|awk -F'|' '{print $1}'`
	echo "#Please remove the extra | in the tweet starting with \"$date\" and reschedule the tweet." >>tweet.txt
	continue
  fi
  date=`echo $line|awk -F'|' '{print $1}'`
  user=`echo $line|awk -F'|' '{print $2}'`
  tweet=`echo $line|awk -F'|' '{print $3}'`
  access_token=`grep "^$user:" tweet.conf|awk -F: '{print $2}'`
  access_token_secret=`grep "^$user:" tweet.conf|awk -F: '{print $3}'`
  php tweet.php "$tweet" $access_token $access_token_secret $consumer_key $consumer_secret
  if [ $? -eq 0 ] ; then
    grep "^$line$" tweet.txt >>completedtweets.txt
    grep -v "^$line$" tweet.txt >$$.x
    mv $$.x tweet.txt
  fi
done
