#!/usr/bin/python

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

# Fix up p443san - but was that p587san overwrote p443san when both
# were present. Fix is to delve back into records.fresh, pick out 
# the right record, update the p443san and then produce a new 
# collisions.json file. After that, usual make targets can be used
# to recrate graphs etc. as desired and they should be the same.

# For the IE-20180316 run, we need to check/fix 2959 from 9765 records

import os, sys, argparse, tempfile, gc
import json
import jsonpickle # install via  "$ sudo pip install -U jsonpickle"
import time, datetime
from dateutil import parser as dparser  # for parsing time from comand line and certs
import pytz # for adding back TZ info to allow comparisons

# our own stuff
from SurveyFuncs import *  

# default values
infile="records.fresh"
outfile="collisions.json"

# command line arg handling 
argparser=argparse.ArgumentParser(description='Fix mcuked-up p443san records for collisions')
argparser.add_argument('-i','--input',     
                    dest='infile',
                    help='file containing previously generated collisions')
argparser.add_argument('-o','--output_file',     
                    dest='outfile',
                    help='file in which to put fixed json records')
args=argparser.parse_args()

def usage():
    print >>sys.stderr, "usage: " + sys.argv[0] + " -i <infile> -o <putfile> "
    print >>sys.stderr, "    both inputs are mandatory and must differ"

if args.infile is None:
    print "You need to supply all inputs"
    usage()

infile=args.infile

if args.outfile is None:
    print "You need to supply all inputs"
    usage()

outfile=args.outfile

if infile==outfile:
    print "can't overwrite input with output"
    usage()

def certfromrf(ip):
    # will do real code here shortly...
    print "\t\tChecking for " + ip
    return None

# fixup function
def fix443names(f):
    # grab f.ip record p443 server cert from records.fresh into cert
    cert=certfromrf(f.ip)
    if cert is None:
        return False
    return True
    nameset=f.analysis['nameset']
    portstring='p443'
    dn=cert['parsed']['subject_dn'] 
    dn_fqdn=dn2cn(dn)
    nameset[portstring+'dn'] = dn_fqdn
    # name from cert SAN
    # zap old sans
    oldsancount=0
    elname='p442san'+str(sancount) 
    while elname in nameset:
        nameset.remove(elname)
        sancount += 1
        elname='p442san'+str(sancount) 
    # and repair from cert
    if 'subject_alt_name' in cert['parsed']['extensions']:
        sans=cert['parsed']['extensions']['subject_alt_name'] 
        san_fqdns=sans['dns_names']
        # we ignore all non dns_names - there are very few in our data (maybe 145 / 12000)
        # and they're mostly otherName with opaque OID/value so not that useful. (A few
        # are emails but we'll skip 'em for now)
        #print "FQDN san " + str(san_fqdns) 
        sancount=0
        for san in san_fqdns:
            nameset[portstring+'san'+str(sancount)]=san_fqdns[sancount]
            sancount += 1
            # there are some CRAAAAAAZZZY huge certs out there - saw one with >1500 SANs
            # which slows us down loads, so we'll just max out at 20
            if sancount >= 20:
                toobig=str(len(san_fqdns))
                nameset['san'+str(sancount+1)]="Bollox-eoo-many-sans-1-" + toobig
                print >> sys.stderr, "Too many bleeding ( " + tobig + ") sans "
                break
    return True

# mainline processing

# open file
fp=open(infile,"r")
jsonpickle.set_encoder_options('json', sort_keys=True, indent=2)

overallcount=0
checkcount=0
fixcount=0

f=getnextfprint(fp)
while f:

    if ('p443dn' in f.analysis['nameset']) and ('p587dn' in f.analysis['nameset']):
        checkcount += 1
        if fix443names(f):
            fixcount += 1

    if overallcount % 100 == 0:
        print >> sys.stderr, "Repairing colisions, did: " + str(overallcount) + " checked: " + str(checkcount) + " fixed: " + str(fixcount)

    f=getnextfprint(fp)
    overallcount += 1

fp.close()

print >> sys.stderr, "Done repairing colisions, did: " + str(overallcount) + " checked: " + str(checkcount) + " fixed: " + str(fixcount)