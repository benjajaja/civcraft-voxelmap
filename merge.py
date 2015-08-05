import os
import time
import sys
import shutil
import math
from subprocess import call
import pdb
import zipfile
from tqdm import *

dir = sys.argv[1]

BIOME_INDEX = 16

if not os.path.exists("master"):
	os.makedirs("master")

def isEmptyColumn(bytes, index):
	return bytes[index + 8] == 0 or bytes[index + BIOME_INDEX] == 28


def merge(sourceBytes, destBytes, overwrite):
	index = 0
	for x in range(0, 256 * 256):
		if not isEmptyColumn(sourceBytes, index):
			if overwrite or isEmptyColumn(destBytes, index):
				destBytes[index:index + 17] = sourceBytes[index:index + 17]

		index += 17

timestamps = {}
if os.path.exists("timestamps"):
	tsFile = open("timestamps", "r")
	for line in tsFile:
		[coords, timestamp] = line.split(":")
		timestamps[coords] = float(timestamp)
	tsFile.close()
else:
	print "warning: no timestamp file present"


def update_progress(progress):
	barLength = 20 # Modify this to change the length of the progress bar
	block = int(round(barLength*progress))
	text = "\rComplete: [{0}] {1}%".format( "="*block + " "*(barLength-block), round(progress*100))
	sys.stdout.write(text)
	sys.stdout.flush()

size = 60
for y in range(size * -1, size):
	update_progress(float(y + size + 1) / (size * 2))
	for x in range(size * -1, size):
		source = "%s/%d,%d.zip" % (dir, x, y)
		dest = "master/%d,%d.zip" % (x, y)
		if not os.path.exists(source):
			continue

		if not os.path.exists(dest):
			shutil.copyfile(source, dest)
			timestamps["%d,%d" % (x, y)] = int(os.path.getmtime(source))
			continue

		sourceBytes = bytearray()
		zip = zipfile.ZipFile(source, "r")
		sourceBytes.extend(zip.read("data"))
		zip.close()

		sourceTime = timestamps["%d,%d" % (x, y)] if "%d,%d" % (x, y) in timestamps else os.path.getmtime(source)

		destBytes = bytearray()
		zip = zipfile.ZipFile(dest, "r")
		destBytes.extend(zip.read("data"))
		zip.close()
		destTime = os.path.getmtime(dest)

		overwrite = sourceTime > destTime

		merge(sourceBytes, destBytes, overwrite)

		zip = zipfile.ZipFile(dest, "w")
		zip.writestr("data", buffer(destBytes))
		zip.close()

		timestamps["%d,%d" % (x, y)] = int(sourceTime if overwrite else destTime)

tsFile = open("timestamps", "w")
for attr, value in timestamps.iteritems():
	tsFile.write("%s:%d\n" % (attr, value))
tsFile.close()
