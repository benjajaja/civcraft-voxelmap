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

if os.path.exists("biomes"):
	shutil.rmtree("biomes")
os.makedirs("biomes");
if os.path.exists("height"):
	shutil.rmtree("height")
os.makedirs("height");

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
def getColor(bytes, maptype, x, y):

	if maptype == "biomes":
		return palettes.BIOME_COLOR_MAP[bytes[BIOME_INDEX]]
	else: # heightmap
		if bytes[2] == 9 or bytes[2] == 8: # water
			# in theory, we could encode both surface height and depth in the color
			return (max(0, bytes[0] - 64), 0, min(255, bytes[4] * 4), 255)
		else:
			return (max(0, bytes[0] * 2 - 256), min(255, bytes[0] * 2), 0, 255)

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
				color = getColor(bytes[index:index + 17], maptype, x, y)

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
	update_progress(float(y + size + 1) / (size * 2))
	for x in range(size * -1, size):

		source = "%s/%d,%d.zip" % (dir, x, y);
		if not os.path.exists(source):
			continue

		string = zipfile.ZipFile(source).read("data");
		bytes = bytearray();
		bytes.extend(string)

		for maptype in ["biomes", "height"]:
			dest = "%s/%d,%d.png" % (maptype, x, y);

			pixels = getPixels(bytes, maptype);
			image = png.from_array(pixels, "RGBA", {'height': 256, 'width': 256});
			image.save(dest);
