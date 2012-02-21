#!/usr/bin/env python

import commands
import re
import operator
import sys

path = '.'
if (len(sys.argv) > 1):
	path = sys.argv[1]

print "Path: " + path

git_ls_cmd = 'git ls-tree --name-only HEAD ' + path + ' | egrep "\.m$|\.h$"'
filelist = commands.getoutput(git_ls_cmd).split('\n');

name_dict = { }

for filename in filelist:
	if filename == '':
		break
	blamelist = commands.getoutput("git blame " + filename).split('\n')
	for line in blamelist:
		#print line
		components = re.findall("(\^?[0-9A-Fa-f]{7,8}).+\((.*) +(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2} (\+|-)\d{4}) +[0-9]+\) (.*)", line)[0]
		if not re.match("^[ \t]*$", components[3]):
			#print components[1]
			name = components[1].strip()
			if name in name_dict:
				name_dict[name] = name_dict[name] + 1
			else:
				name_dict[name] = 1
	

sum_lines = 0
for name, count in name_dict.iteritems():
	sum_lines += count

sorted_name_tuple = sorted(name_dict.iteritems(), key=operator.itemgetter(1), reverse=True)

for name_tuple in sorted_name_tuple:
	print '{0:>25}: {1:5} {2:6.2%}'.format(name_tuple[0], name_tuple[1], name_tuple[1] / float(sum_lines))

print '\n{0:>25}: {1:5}'.format("Total lines", sum_lines)

