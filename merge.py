import os
import time
import sys
import shutil
from subprocess import call
import pdb
import zipfile
import png

dir = sys.argv[1];
maptype = sys.argv[2];

BIOME_INDEX = 16;

BIOME_COLOR_MAP = {
	"0": "Ocean",
	"1": "Plains",
	"2": "Desert",
	"3": "Extreme Hills",
	"4": "Forest",
	"5": "Taiga",
	"6": "Swampland",
	"7": "River",
	"8": "Nether",
	"9": "End",
	"10": "Frozen Ocean",
	"11": "Frozen River",
	"12": "Ice Plains",
	"13": "Ice Mountains",
	"14": "Mushroom Island",
	"15": "Mushroom Island Shore",
	"16": "Beach",
	"17": "Desert Hills",
	"18": "Forest Hills",
	"19": "Taiga Hills",
	"20": "Extreme Hills Edge",
	"21": "Jungle",
	"22": "Jungle Hills",
	"23": "Jungle Edge",
	"24": "Deep Ocean",
	"25": "Stone Beach",
	"26": "Cold Beach",
	"27": "Birch Forest",
	"28": "Birch Forest Hills",
	"29": "Roofed Forest",
	"30": "Cold Taiga",
	"31": "Cold Taiga Hills",
	"32": "Mega Taiga",
	"33": "Mega Taiga Hills",
	"34": "Extreme Hills+",
	"35": "Savanna",
	"36": "Savanna Plateau",
	"37": "Mesa",
	"38": "Mesa Plateau F",
	"39": "Mesa Plateau",
	"129": "Sunflower Plains",
	"130": "Desert M",
	"131": "Extreme Hills M",
	"132": "Flower Forest",
	"133": "Taiga M",
	"134": "Swampland M",
	"140": "Ice Plains Spikes",
	"149": "Jungle M",
	"151": "Jungle Edge M",
	"155": "Birch Forest M",
	"156": "Birch Forest Hills M",
	"157": "Roofed Forest M",
	"158": "Cold Taiga M",
	"160": "Mega Spruce Taiga",
	"161": "Redwood Taiga Hills M",
	"162": "Extreme Hills+ M",
	"163": "Savanna M",
	"164": "Savanna Plateau M",
	"165": "Mesa (Bryce)",
	"166": "Mesa Plateau F M",
	"167": "Mesa Plateau M",
}
COLORMAP = [
[ "Cold Taiga M", { "r":89, "g":125, "b":114 } ],
[ "Desert", { "r":250, "g":148, "b":24 } ],
[ "Mushroom Island Shore", { "r":160, "g":0, "b":255 } ],
[ "Taiga", { "r":11, "g":102, "b":89 } ],
[ "Extreme Hills Edge M", { "r":154, "g":160, "b":194 } ],
[ "Cold Beach M", { "r":255, "g":255, "b":232 } ],
[ "Mesa Plateau", { "r":202, "g":140, "b":101 } ],
[ "Birch Forest Hills M", { "r":71, "g":135, "b":90 } ],
[ "Ice Mountains", { "r":160, "g":160, "b":160 } ],
[ "Swampland M", { "r":47, "g":255, "b":218 } ],
[ "Mushroom Island M", { "r":255, "g":40, "b":255 } ],
[ "Birch Forest Hills", { "r":31, "g":95, "b":50 } ],
[ "Extreme Hills+ M", { "r":120, "g":152, "b":120 } ],
[ "Taiga M", { "r":51, "g":142, "b":129 } ],
[ "Jungle M", { "r":123, "g":163, "b":49 } ],
[ "Mega Spruce Taiga (Hills)", { "r":109, "g":119, "b":102 } ],
[ "Savanna", { "r":189, "g":178, "b":95 } ],
[ "Roofed Forest M", { "r":104, "g":121, "b":66 } ],
[ "Mesa Plateau F", { "r":176, "g":151, "b":101 } ],
[ "Mesa Plateau F M", { "r":216, "g":191, "b":141 } ],
[ "Ice Mountains M", { "r":200, "g":200, "b":200 } ],
[ "Mega Taiga Hills", { "r":69, "g":79, "b":62 } ],
[ "Redwood Taiga Hills M", { "r":69, "g":79, "b":62 } ],
[ "Ice Plains Spikes", { "r":180, "g":220, "b":220 } ],
[ "Mushroom Island Shore M", { "r":200, "g":40, "b":255 } ],
[ "Deep Ocean M", { "r":40, "g":40, "b":88 } ],
[ "Ice Plains", { "r":255, "g":255, "b":255 } ],
[ "Mesa Plateau M", { "r":242, "g":180, "b":141 } ],
[ "Cold Taiga Hills M", { "r":76, "g":103, "b":94 } ],
[ "Frozen River", { "r":160, "g":160, "b":255 } ],
[ "Frozen River M", { "r":200, "g":200, "b":255 } ],
[ "Forest", { "r":5, "g":102, "b":33 } ],
[ "Mesa (Bryce)", { "r":255, "g":109, "b":61 } ],
[ "Frozen Ocean", { "r":144, "g":144, "b":160 } ],
[ "Forest Hills", { "r":34, "g":85, "b":28 } ],
[ "Mega Spruce Taiga", { "r":129, "g":142, "b":121 } ],
[ "Beach", { "r":250, "g":222, "b":85 } ],
[ "Desert Hills", { "r":210, "g":95, "b":18 } ],
[ "Roofed Forest", { "r":64, "g":81, "b":26 } ],
[ "Nether M", { "r":255, "g":40, "b":40 } ],
[ "Stone Beach", { "r":162, "g":162, "b":132 } ],
[ "Extreme Hills M", { "r":136, "g":136, "b":136 } ],
[ "Desert M", { "r":255, "g":188, "b":64 } ],
[ "Deep Ocean", { "r":0, "g":0, "b":48 } ],
[ "Extreme Hills", { "r":96, "g":96, "b":96 } ],
[ "Jungle Hills M", { "r":84, "g":106, "b":45 } ],
[ "Jungle", { "r":83, "g":123, "b":9 } ],
[ "Taiga Hills M", { "r":62, "g":97, "b":91 } ],
[ "Ocean M", { "r":40, "g":40, "b":152 } ],
[ "Savanna Plateau", { "r":167, "g":157, "b":100 } ],
[ "Extreme Hills Edge", { "r":114, "g":120, "b":154 } ],
[ "End", { "r":128, "g":128, "b":255 } ],
[ "Mushroom Island", { "r":255, "g":0, "b":255 } ],
[ "Birch Forest", { "r":48, "g":116, "b":68 } ],
[ "Mesa", { "r":217, "g":69, "b":21 } ],
[ "Mega Taiga", { "r":89, "g":102, "b":81 } ],
[ "Savanna M", { "r":229, "g":218, "b":135 } ],
[ "River", { "r":0, "g":0, "b":255 } ],
[ "Swampland", { "r":7, "g":249, "b":178 } ],
[ "Sunflower Plains", { "r":181, "g":219, "b":136 } ],
[ "Extreme Hills+", { "r":80, "g":112, "b":80 } ],
[ "River M", { "r":40, "g":40, "b":255 } ],
[ "Flower Forest", { "r":45, "g":142, "b":73 } ],
[ "Ocean", { "r":0, "g":0, "b":112 } ],
[ "Plains", { "r":141, "g":179, "b":96 } ],
[ "Beach M", { "r":255, "g":255, "b":125 } ],
[ "Sky M", { "r":168, "g":168, "b":255 } ],
[ "Nether", { "r":255, "g":0, "b":0 } ],
[ "Taiga Hills", { "r":22, "g":57, "b":51 } ],
[ "Jungle Edge M", { "r":138, "g":179, "b":63 } ],
[ "Cold Taiga", { "r":49, "g":85, "b":74 } ],
[ "Forest Hills M", { "r":74, "g":125, "b":68 } ],
[ "Jungle Edge", { "r":98, "g":139, "b":23 } ],
[ "Birch Forest M", { "r":88, "g":156, "b":108 } ],
[ "Jungle Hills", { "r":44, "g":66, "b":5 } ],
[ "Stone Beach M", { "r":202, "g":202, "b":172 } ],
[ "Desert Hills M", { "r":250, "g":135, "b":58 } ],
[ "Frozen Ocean M", { "r":184, "g":184, "b":200 } ],
[ "Savanna Plateau M", { "r":207, "g":197, "b":140 } ],
[ "Cold Taiga Hills", { "r":36, "g":63, "b":54 } ],
[ "Cold Beach", { "r":250, "g":240, "b":192 } ] ];

for attr, value in BIOME_COLOR_MAP.iteritems():
	for biome in COLORMAP:
		if biome[0] == value:
			color = biome[1];
			BIOME_COLOR_MAP[attr] = (color["r"], color["g"], color["b"], 255);
			break;

	if isinstance(BIOME_COLOR_MAP[attr], str):
		print BIOME_COLOR_MAP[attr];

def getColor(bytes, index):
	if maptype == "biomes":
		return BIOME_COLOR_MAP[str(bytes[index + BIOME_INDEX])];
	else: # heightmap
		if bytes[index + 2] == 9 or bytes[index + 2] == 8: # water
			# in theory, we could encode both surface height and depth in the color
			return (0, 0, min(255, bytes[index + 4] * 4), 255);
		else:
			return (max(0, bytes[index + 0] * 2 - 256), min(255, bytes[index + 0] * 2), 0, 255);

def getPixels(bytes):
	pixels = [];
	index = 0;
	for x in range(0, 256):
		row = [];
		for y in range(0, 256):
			if bytes[index + 8] == 0 or bytes[index + BIOME_INDEX] == 28:
				 # highest rain blocking block cannot be AIR, it means there is no data
				 # if biome is 28 "Birch Forest Hills", that biome doesn't exist on civcraft and is weird imported data
				color = (0, 0, 0, 0);
			else:
				color = getColor(bytes, index);

			row.append(color);
			index += 17;
		pixels.append(row);

	return pixels;

for x in range(-60, 60):
	for y in range(-60, 60):
		print "%s,%s" % (x, y);
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
