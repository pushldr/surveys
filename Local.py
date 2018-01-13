#!/usr/bin/python

# this starts to classify the output file we got back from
# CensysIESMTP.py
# this one just tries to see if the enrties are really local

import sys
import json
import socket

# figure out what names apply - just printing for now, decide
# on a winner later
def p_fqdn(p25,ip):
    try:
        try:
            # name from reverse DNS
            rdnsrec=socket.gethostbyaddr(ip)
            rdns=rdnsrec[0]
            print "FQDN reverse: " + rdns
        except:
            print "FQDN reverse exception" + str(e)
        # try name from banner
        banner=p25['smtp']['starttls']['banner'] 
        ts=banner.split()
        banner_fqdn=ts[1]
        rip=socket.gethostbyname(banner_fqdn)
        if rip == ip:
            print "FQDN (verified): " + banner_fqdn + " (" + rip + ")"
        else:
            print "FQDN (failed): " + banner_fqdn + " (" + rip + " != " + ip + ")"
        return True
    except Exception as e: 
        print "FQDN p_fqdn exception" + str(e)
        return False
    return False

def p_banner(p25):
    try:
        print "banner: " + p25['smtp']['starttls']['banner'] ;
        return True
    except:
        return False
    return False

def p_ehlo(p25):
    try:
        print "ehlo: " + p25['smtp']['starttls']['ehlo'] ;
        return True
    except:
        return False
    return False

def p_starttlsbanner(p25):
    try:
        print "starttls: " + p25['smtp']['starttls']['starttls'] ;
        return True
    except:
        return False
    return False

bads={}

with open(sys.argv[1],'r') as f:
    overallcount=0
    badcount=0
    goodcount=0
    bannercount=0
    for line in f:
        j_content = json.loads(line)
        p25=j_content['p25']
        print "\nRecord: " + str(overallcount) + ":"
        dodgy=False
        if not p_fqdn(p25,j_content['ip']):
            dodgy=True
        if not p_banner(p25):
            dodgy=True
        if not p_starttlsbanner(p25):
            dodgy=True
        if not p_ehlo(p25):
            dodgy=True
        if not dodgy:
            goodcount += 1
        else:
            bads[badcount]=j_content
            badcount += 1
        overallcount += 1
        if overallcount % 100 == 0:
            # exit early for debug purposes
            #break
            print "Did : " + str(overallcount)

# this gets crapped on each time (for now)
badf=open('dodgy.json', 'w')
badf.write(json.dumps(bads) + '\n')
badf.close()

print "overall: " + str(overallcount) + " good: " + str(goodcount) + " bad: " + str(badcount) + "\n"