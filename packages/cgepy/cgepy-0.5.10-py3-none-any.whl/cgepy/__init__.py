__version__ = '0.5.10'
try:
	from cgePy.cgepy.codes import *
	from cgePy.cgepy import cust
except ModuleNotFoundError:
	try:
		from cgepy.cgepy.codes import *
		from cgepy.cgepy import cust
	except ModuleNotFoundError:
		from cgepy.codes import *
		from cgepy import cust
def cs():
	print("\033[2J")
	print("\033[H")


spritecolor = RED
background = BLUE
gridsize = 100

currentlyin = 0
gridinfo = {}

pr = int(gridsize**0.5)
class cge:
	ctx = []
	class Exceptions:
		class OutOfRangeError(Exception):
			pass
		class MapError(Exception):
			pass
	class legacy:
		def cleargrid():
			counter=0
			newmap=[]
			for i in range(gridsize):
				newmap.append(background+"  ")
			return newmap
			
		def creategrid():
			counter=0
			newmap=[]
			for i in range(gridsize):
				newmap.append(background+"  ")
			return newmap
		def updategrid(grid=""):
			cs()
			if grid != "":
				cm = grid
				grid = cm
			if grid == "":
				raise Exception("cgePy: Error updating grid.\nIf you are trying to paint a map,\nplease try again later (feature currently unavailable)")
			grid[currentlyin%gridsize]=spritecolor+"  "
			counter=-1
			refr=-1
			cs()
			for i in range(0,gridsize):
				counter+=1
				refr+=1
				if refr == pr:
					if refr == gridsize-pr:
						refr = 1
						print("")
					else:
						print("")
						refr=0
				print(grid[counter], end="")
			print(white+"")
		def updatepos(newpos):
			global currentlyin
			try:
				cm[currentlyin] = background+"  "
			except IndexError:
				pass
			currentlyin = newpos
		def movepos(direction):
			global currentlyin
			try:
				cm[gridsize] = background+"  "
			except IndexError:
				pass
			if direction == "up":
				currentlyin-=pr
			if direction == "down":
				currentlyin+=pr
			if direction == "left":
				currentlyin-=1
			if direction == "right":
				currentlyin+=1
		def paint(map):
			counter = -1
			paintedlist = []
			#remove spacing
			counter=-1
			odd = 0
			map = map.replace(" ","")
			map = map.replace(",","")
			map = map.replace("\n","")
			map = map.replace("BG",background+"  ,")
			map = map.replace("RE",RED+"  ,")
			map = map.replace("YE",YELLOW+"  ,")
			map = map.replace("GR",GREEN+"  ,")
			map = map.replace("BL",BLUE+"  ,")
			map = map.replace("CY",CYAN+" ,")
			map = map.replace("MA",MAGENTA+"  ,")
			map = map.replace("BB",BLACK+"  ,")
			map = map.replace("WH",WHITE+"  ,")
			map = map.replace("RR",RESET+"  ,")
			map = map.split(",")
			return map
class Grid:
	def __init__(self, ctx="", new=True):
		self.ctx = ctx
		if new == True:
			self.ctx = cge.legacy.creategrid()
		else:
			if new == list():
				self.ctx = new
			elif new == Grid:
				self.ctx = new.ctx
			else:
				try:
					self.ctx == new.main
				except AttributeError:
					self.ctx == new
	def clear(self):
		self.ctx = cge.legacy.creategrid()
	def write(self, pos, new):
		try:
			self.ctx[pos] = new
		except IndexError:
			raise cge.Exceptions.OutOfRangeError
	def swap(self, new):
		self.ctx = new
	def Update(self):
		cge.legacy.updategrid(self.ctx)
	def Self(self):
		return self.ctx
class Map:
	def __init__(self, map=False):
		if map==False:
			self.main = '''undefined'''
		else:
			self.main = map
	def Paint(self):
		if self.main == '''undefined''':
			raise cge.Exceptions.MapError("Cannot paint an undefined map.")
		else:
			self.ctx = cge.legacy.paint(self.main)
			del self.main
			self.__class__ = Grid
class Sprite:
	def __init__(self,pos=0,color=RED):
		self.pos = pos
		self.color = color
		self.sprite = color+"  "
	def Color(self,color):
		self.color = color
		self.sprite = color+"  "
	def Move(self,dir):
		if dir.lower() == "up":
			self.pos -= pr
		if dir.lower() == "down":
			self.pos += pr
		if dir.lower() == "left":
			self.pos -= 1
		if dir.lower() == "right":
			self.pos += 1

class MainSprite:
	def __init__(self):
		spritecolor = RED
	def Color(self,color):
		spritecolor = color
	def Move(self,dir):
		if dir.lower() == "up":
			cge.legacy.movepos("up")
		if dir.lower() == "down":
			cge.legacy.movepos("down")
		if dir.lower() == "left":
			cge.legacy.movepos("left")
		if dir.lower() == "right":
			cge.legacy.movepos("right")
			
MainSprite1 = MainSprite()
del MainSprite
MainSprite = MainSprite1
del MainSprite1