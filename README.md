# surveys

Code for various crypto-survey related stuff. 

My first article based on this code is [here](https://eprint.iacr.org/2018/299).

## Overview

The current code collects and collates server cryptographic keys (SSH and TLS)
from hosts in a specified country that listen on port 25 (so are mail servers)
and then sees which of those are re-using keys for SSH or TLS ports.

- ```install-deps.sh``` is a first cut at an installer for dependencies

- Then you need to select a list of IPv4 addresses, eiter from a previous
run or from MaxMind for some country code, e.g. "IE".

- ```skey-all.sh``` is the script to orchestrate things

- The local ```Makefile``` can be used for bits'n'pieces in various ways

- Most of the main code is the top directory of the repo for now. That
includes the main python scripts as described below.

- The ```clustertools``` directory has additional scripts to analyse clusters.

- The ```misc``` directory has various bits and pieces knocked up along the way
  in case they prove handy later. Those should be ignorable.

## Using it

1. Pick a host from which to scan. Ensure you do this from a host that can make
   outbound port 25 connections - if it can't, you'll miss out on those! 

1. Pick a top level directory where you're going to run things, let's call that
```$TOP```. Usually I use ```$HOME/data/smtp/runs/``` but it should work
elsewhere. The main script will create per-run directories below that, in which
the various scan and log files will be created.

1. I assume that this repo's main directory has been added to your ```$PATH``` but
refer to it as ```$REPO``` as necessary below.

1. Install dependencies:

		$ install-deps.sh 
		... lots of output ...

1. Update the MaxMind database if it's been a while since you rand the install.
   The latest databases for that are kept in the ```$REPO/mmdb/``` directory.

		$ mm_update.sh
		... lots of output ...

1. Pick a country and start the scan. You need the two-letter code for that,
   e.g., "IE"  and to tell the ```skey-all.sh``` script, and to use MaxMind
(```-mm```) to generate a list of prefixes. You also need to tell the script
where to put the output (```-r .``` in this case). Once this is working ok, then
you'll want to run it via nohup, as it takes a long time.

		$ cd $TOP
		$ nohup skey-all.sh -c IE -mm >skey.out -r . 2>&1 &
		$ 

	You'll see a directory created below ```$TOP``` to contain
	the run files, that'll be names something like ```IE-20180423-161002```

1. Go out for the evening... It *might* all just work:-)

1. If you're impatient, you can watch progress in a log file that's
in the run directory. With the same example you'd be doing this:

		$ tail -f IE-20180423-161002/20180423-161002.out
		 4:33 3% (2h44m left); send: 38600 148 p/s (140 p/s avg); recv: 169 2 p/s (0 p/s avg); drops: 0 p/s (0 p/s avg); hitrate: 0.44%
		 4:34 3% (2h44m left); send: 38748 147 p/s (140 p/s avg); recv: 169 0 p/s (0 p/s avg); drops: 0 p/s (0 p/s avg); hitrate: 0.44%
		 4:35 3% (2h44m left); send: 38888 139 p/s (140 p/s avg); recv: 170 0 p/s (0 p/s avg); drops: 0 p/s (0 p/s avg); hitrate: 0.44%
		 4:36 3% (2h44m left); send: 39036 147 p/s (141 p/s avg); recv: 172 1 p/s (0 p/s avg); drops: 0 p/s (0 p/s avg); hitrate: 0.44%
		 4:37 3% (2h44m left); send: 39192 145 p/s (141 p/s avg); recv: 172 0 p/s (0 p/s avg); drops: 0 p/s (0 p/s avg); hitrate: 0.44%
		 4:38 3% (2h44m left); send: 39338 145 p/s (141 p/s avg); recv: 174 1 p/s (0 p/s avg); drops: 0 p/s (0 p/s avg); hitrate: 0.44%
		 4:39 3% (2h44m left); send: 39481 142 p/s (141 p/s avg); recv: 175 0 p/s (0 p/s avg);......

	The "2h44m left" timing that ZMap produces is pretty accurate. The "recv: 175" on the last 
	line means that ZMap has found 175 port 25 listeners. For the rest, see the ZMap man page.


