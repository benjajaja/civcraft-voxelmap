import os
import time
import sys
import shutil
from subprocess import call
import pdb
import zipfile
import png
from tqdm import *
import palettes

dir = "master";
maptype = sys.argv[1];

BIOME_INDEX = 16;


def getColor(bytes, index):
	if maptype == "biomes":
		return palettes.BIOME_COLOR_MAP[bytes[index + BIOME_INDEX]];
	else: # heightmap
		if bytes[index + 2] == 9 or bytes[index + 2] == 8: # water
			# in theory, we could encode both surface height and depth in the color
			return (0, 0, min(255, bytes[index + 4] * 4), 255);
		else:
			return (max(0, bytes[index + 0] * 2 - 256), min(255, bytes[index + 0] * 2), 0, 255);

def getPixels(bytes):
	pixels = [];
	index = 0;
	for x in range(0, 256 * 256):
		if bytes[index + 8] == 0 or bytes[index + BIOME_INDEX] == 28:
			 # highest rain blocking block cannot be AIR, it means there is no data
			 # if biome is 28 "Birch Forest Hills", that biome doesn't exist on civcraft and is weird imported data
			color = (0, 0, 0, 0);
		else:
			color = getColor(bytes, index);

		index += 17;
		pixels.append(color);

	return pixels;
size = 60;
for i in tqdm(range(size * size * 4)):
	x = int(i / size) - size;
	y = i % size - size;

	source = "%s/%d,%d.zip" % (dir, x, y);
	dest = "%s/%d,%d.png" % (maptype, x, y);
	if not os.path.exists(source):
		continue

	string = zipfile.ZipFile(source).read("data");
	bytes = bytearray();
	bytes.extend(string)
	pixels = getPixels(bytes);
	image = png.from_array(pixels, "RGBA");
	image.save(dest);
