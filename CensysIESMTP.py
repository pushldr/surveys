#!/usr/bin/python

# censys.io sample API code from https://censys.io/api

# you need specific permission to use the export API
# I'm just figuring out how to get it to work still
# so don't believe this code:-)

import censys.export

# CensysApiKey.py should have lines like these with your a/c 
# specific values, that your find at: https://censys.io/account
# UID = "9b611dbd-366b-41b1-a50e-1a024004609f"
# SECRET = "wAUW4Ax9uyCkD7JrgS1ItJE5nHQD5DnR"

from CensysApiKey import UID, SECRET

c = censys.export.CensysExport(UID,SECRET)

# Start new Job - all Irish smtp speakers
# works
#res = c.new_job('select * from ipv4.20170915 where ip="185.24.233.211"')
# fails - get invalid timestamp value after ~20s
#res = c.new_job('select * from ipv4.20170914 where location.country_code="IE" and p25.smtp.starttls.banner IS NOT NULL')
# works we get 12580
#res = c.new_job('select count(ip) from ipv4.20170914 where location.country_code="IE" and tags contains "smtp"')
res = c.new_job('select * from ipv4.20170914 where location.country_code="IE" and tags contains "smtp"')

job_id = res["job_id"]

# Wait for job to finish and fetch results
print c.check_job_loop(job_id)

