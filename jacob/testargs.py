import sys

for i in range(len(sys.argv)):
  print str(sys.argv[i].split('/')[-1])


