#!/bin/bash

# Copyright (C) 2018 Stephen Farrell, stephen.farrell@cs.tcd.ie
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

# grab and explode updated versions of maxmind's free DBs

set -x

# for testing
#skipwget=false
#if [ "$1" == "SkipWget" ]
#then
	#skipwget=true
#fi

# just configure that directory in one place
DESTDIR=`grep mmdbdir $HOME/code/surveys/SurveyFuncs.py  | head -1 | awk -F\' '{print $2}'`
# for testing
#DESTDIR=$PWD/db

TMPD=`mktemp -d /tmp/mmdbXXXX`

pushd $TMPD

for db in City Country ASN
do
	tarball="GeoLite2-$db.tar.gz"
	url="http://geolite.maxmind.com/download/geoip/database/$tarball"
	echo "Getting $url"
	#if (( $skipwget ))
	#then
		wget -q $url
	#else
		#echo "Skipping wget $url as requsted"
	#fi
	if [ "$?" != "0" ]
	then
		echo "Failed to download $url"
	else
		tar xzvf $tarball
		dbdate=`ls -d "GeoLite2-$db"_* | awk -F"_" '{print $2}'`
		dirname="GeoLite2-$db"_"$dbdate"
		fname="GeoLite2-$db"
		cp $dirname/$fname.mmdb $DESTDIR$fname-$dbdate.mmdb
		# update link
		ln -sf $DESTDIR$fname-$dbdate.mmdb $DESTDIR$fname.mmdb
	fi
done

popd
# clean up
rm -rf $TMPD
echo "Done"

