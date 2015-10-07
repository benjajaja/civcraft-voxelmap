import os
import time
import sys
import shutil
from subprocess import call
import pdb
import zipfile
import png
import palettes

dir = "master";

BIOME_INDEX = 16;
HEIGHT_INDEX = 0;
SEA_FLOOR_INDEX = 4;
BLOCKID_INDEX = 2;
BLOCKDATA_INDEX = 1;

if os.path.exists("biomes"):
	shutil.rmtree("biomes")
os.makedirs("biomes");
if os.path.exists("height"):
	shutil.rmtree("height")
os.makedirs("height");
if os.path.exists("surface"):
	shutil.rmtree("surface")
os.makedirs("surface");

# Layer 1: Highest Partially light blocking block (inlcuding lava) 
# 00 - Height (0-255) (java byte = -128 to 127 so value is bitwise-anded with 255) 
# 01 - blockstateID < Bigendian two byte ID 
# 02 - blockstateID < (getIdFromBlock(state.getBlock()) + (state.getBlock().getMetaFromState(state) << 12) - real block id?
# 03 - Lightlevel (blockLight + skyLight *16)

# Layer 2:Sea floor (when first layer is water) 
# 04 - as above 
# 05 - 
# 06 - 
# 07 -

# Layer 3: Highest rain blocking block 
# 08 - as above 
# 09 - 
# 10 - 
# 11 -

# Layer 4:vegetation (one block above first layer/// flowers/torches) 
# 12 -as above 
# 13 - 
# 14 - 
# 15 -

# 16 - Biome ID

def surface(bytes):
	id = str(bytes[BLOCKID_INDEX])
	if id in palettes.PALETTE:
		return palettes.PALETTE[id]
	else:
		if not id + ":" + str(bytes[BLOCKDATA_INDEX]) in palettes.PALETTE:
			print "unknown block: %s" % id + ":" + str(bytes[BLOCKDATA_INDEX])
			return palettes.PALETTE["0"]
		else:
			return palettes.PALETTE[id + ":" + str(bytes[BLOCKDATA_INDEX])]

def getColor(bytes, maptype):
	if maptype == "biomes":
		return palettes.BIOME_COLOR_MAP[bytes[BIOME_INDEX]]
	elif maptype == "surface":
		return surface(bytes)
	else: # heightmap
		if bytes[BLOCKID_INDEX] == 9 or bytes[BLOCKID_INDEX] == 8: # water
			# in theory, we could encode both surface height and depth in the color
			return (max(0, bytes[HEIGHT_INDEX] - 64), 0, min(255, bytes[SEA_FLOOR_INDEX] * 4), 255)
		else:
			return (max(0, bytes[HEIGHT_INDEX] * 2 - 256), min(255, bytes[HEIGHT_INDEX] * 2), 0, 255)

def getPixels(bytes, maptype):
	pixels = []
	index = 0
	for x in range(0, 256):
		row = []
		for y in range(0, 256):
			if bytes[index + 8] == 0 or bytes[index + BIOME_INDEX] == 28:
				 # highest rain blocking block cannot be AIR, it means there is no data
				 # if biome is 28 "Birch Forest Hills", that biome doesn't exist on civcraft and is weird imported data
				color = (0, 0, 0, 0)
			else:
				color = getColor(bytes[index:index + 17], maptype)

			index += 17
			row.append(color)
		pixels.append(row)

	return pixels

def update_progress(progress):
    barLength = 20 # Modify this to change the length of the progress bar
    block = int(round(barLength*progress))
    text = "\rComplete: [{0}] {1}%".format( "="*block + " "*(barLength-block), round(progress*100))
    sys.stdout.write(text)
    sys.stdout.flush()

size = 60
for y in range(size * -1, size):
	# update_progress(float(y + size + 1) / (size * 2))
	for x in range(size * -1, size):

		source = "%s/%d,%d.zip" % (dir, x, y);
		if not os.path.exists(source):
			continue

		string = zipfile.ZipFile(source).read("data");
		bytes = bytearray();
		bytes.extend(string)

		# maptypes = ["biomes", "height"]
		maptypes = ["surface"]
		for maptype in maptypes:
			dest = "%s/%d,%d.png" % (maptype, x, y);

			pixels = getPixels(bytes, maptype);
			image = png.from_array(pixels, "RGBA", {'height': 256, 'width': 256});
			image.save(dest);
