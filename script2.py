#!/usr/bin/env python2.7

import subprocess
print(subprocess.call("git status", shell=True))


print(subprocess.call("git diff", shell=True))

print "okay very gud"

print(subprocess.call("git add .", shell=True))
print(subprocess.call("git commit -m hellos ", shell=True))
print(subprocess.call("git push origin four ", shell=True))










