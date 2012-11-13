"""
Sequential number renamer
Creates restore batch file to rename back files.
"""
import sys,os,re

path = '.'
prefix = ''
suffix = ''
frequency = 10000
subdir = ''
matchpattern = r'.*'
base = 1
dbase = 1
restore_rd = False
digits = 4
sortByMod = False

if len(sys.argv) < 2:
	print (
		"usage: " + sys.argv[0] + " [-d path] [-p prefix] [-s suffix] [-S subdir] [-f freq] [-m pattern] [-b base] [-B dbase] [-r]\n"
"""
    All options are optional but at least one option must be specified.
    -d path    Set directory to perform renaming.
    -p prefix  Set prefix for output file name.
    -s suffix  Set suffix for output file name.
    -S subdir  Set prefix for subdirectories.
               If not set, no subdirs will be created.
               If set, every freq files are stored to each subdir.
    -f freq    Set frequency of sequential number.
    -m pattern Set pattern for matching source file names.
    -b base    Set basis of file numbering
    -B dbase   Set basis of subdirectory numbering
    -r         Set to add rmdir command to restore script
    -D digits  Set number of digits, default 4
    -M        Sort by modified time
"""
	)
	quit(0)

# closure to check count of arguments
def chkopt(i):
	if len(sys.argv) <= i + 1:
		print "Premature option: " + val + "\n"
		exit(0)
	i += 1
	return sys.argv[i], i

# interpret command line arguments
i = 1
while i < len(sys.argv):
	val = sys.argv[i]

	# Specifying target directory
	if val == '-d':
		path, i = chkopt(i)

	# Specifying prefix for output file
	elif val == '-p':
		prefix, i = chkopt(i)

	# Specifying suffix for output file
	elif val == '-s':
		suffix, i = chkopt(i)

	# Specifying subdirectory preix
	elif val == '-S':
		subdir, i = chkopt(i)

	# Specifying frequency
	elif val == '-f':
		t, i = chkopt(i)
		frequency = int(t)

	# Specifying source file pattern
	elif val == '-m':
		matchpattern, i = chkopt(i)

	# Specifying base
	elif val == '-b':
		t, i = chkopt(i)
		base = int(t)

	# Specifying dbase
	elif val == '-B':
		t, i = chkopt(i)
		dbase = int(t)

	# Specifying restore_rd
	elif val == '-r':
		restore_rd = True

	# Specifying digits
	elif val == '-D':
		t, i = chkopt(i)
		digits = int(t)

	elif val == '-M':
		sortByMod = True

	else:
		print 'unrecognized option: ' + val

	i += 1


# create restore script
# if we have managed to run the script so far, it means we can run another python script to rename back the files.
# so we generate a restore script not in shell script nor Windows batch file,
# but a script independent of platforms.
restorer = open(os.path.join(path, 'restore.py'), mode='w')
restorer.write("import os\n")

subdirs = []

no=0
files = os.listdir(path)

# Provide predicate to sort by modified date time
if sortByMod:
	files.sort(lambda x,y: cmp(os.stat(os.path.join(path,x)).st_mtime,os.stat(os.path.join(path,y)).st_mtime))
else:
	files.sort()

for i in files:
	# ignore restore script that could exist since the last invocation
	if i == 'restore.bat' or i == 'restore.py':
		continue

	# ignore directories
	if os.path.isdir(i):
		continue

	# ignore files that does not match given pattern
	if not re.match(matchpattern, i):
		continue

	dst = prefix + '%0*d' % (digits, no % frequency + base) + suffix

	# create subdirectory
	if subdir != '':
		subdirname = subdir + ('%04d') % (no / frequency + dbase)
		dst = subdirname + '\\' + dst
		if not os.access(subdirname, os.F_OK):
			os.mkdir(subdirname)
			if restore_rd:
				subdirs.append(subdirname)

	srcpath = os.path.join(path, i)
	dstpath = os.path.join(path, dst)

	print 'rename:' + srcpath + ' -> ' + dstpath
	restorer.write('os.rename("' + dst + '", "' + i + '")\n')
	no += 1
	os.rename(srcpath,dstpath)

for i in subdirs:
	restorer.write('os.rmdir("' + i + "\")\n")
	print 'marked subdir ' + i

restorer.close()

