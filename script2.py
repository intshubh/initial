#!/usr/bin/env python2.7

import os, sys
import argparse
import json
import shutil
import subprocess
from collections import OrderedDict


path='/home/shubhambhatia/Desktop'

#print(os.environ.get['paytm_labs_chef_dir'])
#print(os.environ.get['curr_dir'])
#print(os.environ.get['json_file_dir'])

#print(subprocess.call("git -c color.ui=always diff", shell=True))
print(subprocess.call("git sta"+"tus", shell=True))

#User groupd
'''Dehleez="dehleez-users"
mayassar="grafana-users"
DS4="ds4-users"
new = []
# Define the parser
parser = argparse.ArgumentParser(description='Short sample app')
# Declare an argument (`--algo`), telling that the corresponding value should be stored in the `algo` field, and using a default value if the argument isn't given
parser.add_argument('--algo', action="store", dest='algo', default=0)
parser.add_argument('--fname', action="store", dest='fname', default=0)
parser.add_argument('--lname', action="store", dest='lname', default=0)
parser.add_argument('--list', nargs='+', help='<Required> Set flag', required=True)
# Now, parse the command line arguments and store the values in the `args` variable
args = parser.parse_args()
# Individual arguments can be accessed as attributes...
print args.algo 
print args.fname 
print args.lname
print args.list[0]

new = args.list
print new

for i in new:
	print i



email = raw_input("email here\n")
print email
fn=email.split(".")
first_no = fn[0]
firstname = ''.join(i for i in fn[0] if not i.isdigit())
lastname = fn[1].split("@")[0]
print lastname
print firstname'''

PIPE = subprocess.PIPE
branch = 'shubham'

process = subprocess.Popen(['git', 'pull', branch], stdout=PIPE, stderr=PIPE)
stdoutput, stderroutput = process.communicate()

if 'fatal' in stdoutput:
		print "Handle error case"
else:
		print "Success!"
	
	

     	

shutil.copy2('/home/shubhambhatia/Documents/ram_train', path)



#with open('new.json','r') as f:
        	#listone = json.loads(f.read(), object_pairs_hook=OrderedDict)
		#for a in listone:
		#	print a,listone[a]'''
#os.system("python ldap_json_patch_v2.py firstname lastname email")

#os.chdir(path)

#cwd = os.getcwd()

#print cwd





