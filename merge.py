import os
import time
import sys
import shutil
import math
from subprocess import call
import pdb
import zipfile
from tqdm import *

dir = sys.argv[1];

BIOME_INDEX = 16;


def isEmptyColumn(bytes, index):
	return bytes[index + 8] == 0 or bytes[index + BIOME_INDEX] == 28;


def merge(sourceBytes, destBytes, overwrite):
	index = 0;
	for x in range(0, 256 * 256):
		if not isEmptyColumn(sourceBytes, index):
			if overwrite or isEmptyColumn(destBytes, index):
				destBytes[index:index + 17] = sourceBytes[index:index + 17];

		index += 17;

tsFile = open("timestamps", "r");
timestamps = {};
for line in tsFile:
	[coords, timestamp] = line.split(":");
	timestamps[coords] = float(timestamp);
tsFile.close();

size = 60;
for i in tqdm(range(size * size * 4)):
	x = math.floor(i / size) - size;
	y = i % size - size;

	source = "%s/%d,%d.zip" % (dir, x, y);
	dest = "master/%d,%d.zip" % (x, y);
	if not os.path.exists(source):
		continue

	if not os.path.exists(dest):
		shutil.copyfile(source, dest);
		timestamps["%d,%d" % (x, y)] = int(os.path.getmtime(source));
		continue

	sourceBytes = bytearray();
	zip = zipfile.ZipFile(source, "r");
	sourceBytes.extend(zip.read("data"));
	zip.close();
	sourceTime = timestamps["%d,%d" % (x, y)] if "%d,%d" % (x, y) else os.path.getmtime(source);

	destBytes = bytearray();
	zip = zipfile.ZipFile(dest, "r");
	destBytes.extend(zip.read("data"));
	zip.close();
	destTime = os.path.getmtime(dest);

	overwrite = sourceTime > destTime;

	merge(sourceBytes, destBytes, overwrite);

	zip = zipfile.ZipFile(dest, "w");
	zip.writestr("data", buffer(destBytes));
	zip.close();

	timestamps["%d,%d" % (x, y)] = int(sourceTime if overwrite else destTime);

tsFile = open("timestamps", "w");
for attr, value in timestamps.iteritems():
	tsFile.write("%s:%d\n" % (attr, value));
tsFile.close();
