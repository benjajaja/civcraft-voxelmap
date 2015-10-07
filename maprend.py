

class MapRend(object):
	ColorSource = property()

	def __init__(self, ressourceFolder):
		colorsJSON = None
		arr = colorsJSON.getJSONArray("colors")
		maxID = 0
		i = 0
		while i < arr.length():
			id = arr.getJSONObject(i).getInt("i")
			if id > maxID:
				maxID = id
			i += 1
		self._colors = Array.CreateInstance(int, maxID + 1)
		self._green = Array.CreateInstance(boolean, maxID + 1)
		i = 0
		while i < arr.length():
			cur = arr.getJSONObject(i)
			if cur.getInt("m") == -1:
				j = 0
				while j < 16:
					self._colors[cur.getInt("i")][j] = cur.getInt("c")
					self._green[cur.getInt("i")][j] = (cur.getInt("g") == 1)
					j += 1
			else:
				self._colors[cur.getInt("i")][cur.getInt("m")] = cur.getInt("c")
				self._green[cur.getInt("i")][cur.getInt("m")] = (cur.getInt("g") == 1)
			i += 1


		biomesJSON = None
		biomesArr = biomesJSON.getJSONArray("biomes")
		maxBiomID = 0
		i = 0
		while i < biomesArr.length():
			cur = biomesArr.getJSONObject(i)
			if cur.getInt("id") > maxBiomID:
				maxBiomID = cur.getInt("id")
			i += 1
		self._biomColors = Array.CreateInstance(ColorF, maxBiomID + 1)
		i = 0
		while i < biomesArr.length():
			cur = biomesArr.getJSONObject(i)
			self._biomColors[cur.getInt("id")] = ColorF(1.0f, cur.getDouble("r"), cur.getDouble("g"), cur.getDouble("b"))
			i += 1

	def getColor(self, block, meta, height, light, biome):
		c = self.getBlockColor(block, meta)
		a = 0xff
		r = self.getR(c)
		g = self.getG(c)
		b = self.getB(c)
		heightCoef = ((height) / 255) + 0.5f # * 0.25f + 0.75f;
		r = (r * heightCoef)
		g = (g * heightCoef)
		b = (b * heightCoef)
		lightCoef = (light / 15) * 0.5f + 0.5f
		r = (r * lightCoef)
		g = (g * lightCoef)
		b = (b * lightCoef)
		if self._green[block][meta]:
			biomeCoef = self.biomeCoef(biome)
			r = (r * biomeCoef.getR())
			g = (g * biomeCoef.getG())
			b = (b * biomeCoef.getB())
		if r >= 255:
			r = 255
		if g >= 255:
			g = 255
		if b >= 255:
			b = 255
		return self.getRGBA(r, g, b, a)

	def getBlockColor(self, id, meta):
		return self._colors[id][meta]

	def getRGBA(self, r, g, b, a):
		return (a << 24) | (r << 16) | (g << 8) | b

	def getA(self, color):
		color = color & 0xff000000
		return color >> 24

	def getR(self, color):
		color = color & 0x00ff0000
		return color >> 16

	def getG(self, color):
		color = color & 0x0000ff00
		return color >> 8

	def getB(self, color):
		color = color & 0x000000ff
		return color

	def biomeCoef(self, biome):
		try:
			color = self._biomColors[biome]
			if color == None:
				Console.WriteLine("Null biome: " + biome + ", copying default: 1.")
				self._biomColors[biome] = self._biomColors[1]
				color = self._biomColors[1]
		except System.IndexOutOfRangeException, e:
			Console.WriteLine("Invalid biome: " + biome + ", using default.")
			color = self._biomColors[1]
		finally:
		return color
