#!/usr/bin/env python
import random

class Vec2:
	def __init__(self, x=0, y=0):
		self.x = x
		self.y = y
	def __str__(self):
		return "["+str(self.x)+":"+str(self.y)+"]"
# Tile types:
# 0: end
# 1: I
# 2: L
# 3: T
# 4: +

def GetRotations(type):
	"""Return (integer) how many rotations can have given type of tile"""
	if type == 0:
		return 4
	elif type == 1:
		return 2
	elif type == 2:
		return 4
	elif type == 3:
		return 4
	elif type == 4:
		return 1
	else: return 1

def GetConnections(type, rotation):
	"""Return (array of Vec2) which connections have given type (int) of tile at given rotation (int)"""
	if type == 0:
		if rotation == 0:
			return [Vec2(0,1)]
		elif rotation == 1:
			return [Vec2(-1,0)]
		elif rotation == 2:
			return [Vec2(0,-1)]
		elif rotation == 3:
			return [Vec2(1,0)]
	elif type == 1:
		if (rotation % 2) == 0:
			return [Vec2(0,-1), Vec2(0, 1)]
		else:
			return [Vec2(-1,0), Vec2(1, 0)]
	if type == 2:
		if rotation == 0:
			return [Vec2(0,1), Vec2(1,0)]
		elif rotation == 1:
			return [Vec2(0,1), Vec2(-1,0)]
		elif rotation == 2:
			return [Vec2(0,-1), Vec2(-1,0)]
		elif rotation == 3:
			return [Vec2(0,-1), Vec2(1,0)]
	if type == 3:
		if rotation == 0:
			return [Vec2(0,1), Vec2(0,-1), Vec2(1,0)]
		elif rotation == 1:
			return [Vec2(-1,0), Vec2(1,0), Vec2(0,1)]
		elif rotation == 2:
			return [Vec2(0,1), Vec2(0,-1), Vec2(-1,0)]
		elif rotation == 3:
			return [Vec2(0,-1), Vec2(1,0), Vec2(-1,0)]
	if type == 4:
		return [Vec2(0,1), Vec2(0,-1), Vec2(1,0), Vec2(-1,0)]
	else: return []

def GenerateTileGridA(xx,yy,sx,sy):
	"""
		Generate new random grid of size xx*yy with start at [sx, sy]

		return value is 1d array of Tile
	"""
	grid = []
	tgrid = []
	looseends = []

	for i in range(0,xx*yy):
		grid.append([False,[]])
	
	def XY2I(x,y):
		return x+y*xx
	def I2VEC(i):
		return Vec2(i%xx, i/xx)
	def Tile(x,y):
		return grid[XY2I(x,y)]
	def TTile(x,y):
		return tgrid[XY2I(x,y)]
	def IsAllReachable():
		for i in range(0,xx*yy):
			if grid[i][0] == False:
				return False
		return True
	def IsUnreached(x,y):
		if (not (0 <= x < xx)) or (not (0 <= y < yy)):
			return False
		return  not Tile(x,y)[0]
	def PickOneLooseEndID():
		return random.choice(looseends)
	def PickOneFreeDirectionFromID(i):
		pos = I2VEC(i)
		dirs = [Vec2(-1,0), Vec2(0,1), Vec2(1,0), Vec2(0,-1)]
		random.shuffle(dirs)
		for d in dirs:
			if IsUnreached (pos.x + d.x, pos.y + d.y):
				return d
		else: print "No Free Direction :-X"
	def GridToTGrid():
		del tgrid[:]
		for i in range (0, xx*yy):
			tgrid.append (GetTileFromConnections (grid[i][1]))
		tgrid[XY2I (sx, sy)].accessible = True
		tgrid[XY2I (sx, sy)].start = True
	def PrintGrid():
		GridToTGrid()
		for x in range(0,xx):
			line = ''
			for y in range(0,yy):
				line += str(TTile(y,x))
			print line

	def CleanLooseEnds():
		lc = looseends[:]
		for id in lc:
			DeleteFromLoosendsIfAppropriate(id)
	def DeleteFromLoosendsIfAppropriate(i):
		if not looseends.__contains__(i):
			return
		remove = True
		pos = I2VEC (i)
		for d in [Vec2(-1,0), Vec2(0,1), Vec2(1,0), Vec2(0,-1)]:
			if IsUnreached (pos.x + d.x, pos.y + d.y):
				remove = False
		if remove:
			looseends.remove(i)

	Tile(sx,sy)[0] = True
	looseends.append(XY2I(sx,sy))
	while not IsAllReachable ():
		i = PickOneLooseEndID ()
		direction = PickOneFreeDirectionFromID(i)

		t_pos = I2VEC (i)
		tile = grid[i]

		d_pos = Vec2 (t_pos.x + direction.x, t_pos.y + direction.y)
		d_i = XY2I (d_pos.x, d_pos.y) 
		dtile = grid[d_i]

		dtile[0] = True
		tile[1].append (direction)
		dtile[1].append (Vec2 (0 - direction.x, 0 - direction.y))
		looseends.append(d_i)
		CleanLooseEnds()

	#here we have already grid full, now only convert to hgrid:
	GridToTGrid()
	#PrintGrid()
	return tgrid

def HashToTile(hash):
	if hash[0] == 'u':
		if hash[1] == 'd':
			if hash[2] == 'l':
				if hash[3] == 'r':
					return Tile(4, 0)
				else:
					return Tile(3, 2)
			elif hash[3] == 'r':
				return Tile(3, 0)
			else:
				return Tile(1, 0)
		elif hash[2] == 'l':
			if hash[3] == 'r':
				return Tile(3, 3)
			else:
				return Tile(2, 2)
		elif hash[3] == 'r':
			return Tile(2, 3)
		else:
			return Tile(0, 2)
	elif hash[1] == 'd':
		if hash[2] == 'l':
			if hash[3] == 'r':
				return Tile(3, 1)
			else:
				return Tile(2, 1)
		elif hash[3] == 'r':
			return Tile(2, 0)
		else:
			return Tile(0, 0)
	elif hash[2] == 'l':
		if hash[3] == 'r':
			return Tile(1, 1)
		else:
			return Tile(0, 1)
	elif hash[3] == 'r':
		return Tile(0, 3)
	else: return Tile(4,0)
		
	
def GetTileFromConnections(con):
	"""Convert Connections (array of Vec2) to Tile"""
	class direction:
		def __init__(self):
			self.up = False
			self.down = False
			self.left = False
			self.right = False
		def String(self):
			string = ''
			if self.up: string+='u'
			else: string+='X'
			if self.down:  string+='d'
			else: string+='X'
			if self.left:  string+='l'
			else: string+='X'
			if self.right: string+='r'
			else: string+='X'
			return string
	dir = direction()
	for c in con:
		if c.x == 0:
			if c.y == -1:
				dir.up = True
			elif c.y == 1:
				dir.down = True
		elif c.y == 0:
			if c.x == -1:
				dir.left = True
			elif c.x == 1:
				dir.right = True
	hash = dir.String()
	return HashToTile(hash)


class Tile:
	def __init__(self, type, rotation, accessible=False, start=False):
		self.type = type
		self.rotation = rotation
		self.accessible = accessible
		self.start = False
	def __str__(self):
		if self.type == 0:
			if self.rotation == 0: return 'V'
			if self.rotation == 1: return '<'
			if self.rotation == 2: return '^'
			if self.rotation == 3: return '>'
		if self.type == 1:
			if self.rotation == 0: return '|'
			if self.rotation == 1: return '-'
		if self.type == 2:
			if self.rotation == 0: return 'L'
			if self.rotation == 1: return 'L'
			if self.rotation == 2: return 'L'
			if self.rotation == 3: return 'L'
		if self.type == 3:
			if self.rotation == 0: return 'T'
			if self.rotation == 1: return 'T'
			if self.rotation == 2: return 'T'
			if self.rotation == 3: return 'T'
		if self.type == 4:
			return '+'
		return 'tile'
		
class Grid:
	"""Represents whole grid of pipes"""
	def __init__(self, xx=10, yy=10):
		self.xx = xx
		self.yy = yy
		self.sx = xx/2
		self.sy = yy/2
		self.tiles = GenerateTileGridA(xx, yy, self.sx, self.sy)
		self.Shake()
	
	def UpdateAccess(self):
		"""After rotation of a tile You should call this function to update access info on tiles"""
		looseends = []
		def XY2I(x,y):
			return x+y*self.xx
		def I2VEC(i):
			return Vec2(i%self.xx, i/self.xx)
		def IsConnectedAndValidMove (i_o, dir):
			t_o = self.tiles[i_o]
			pos_o = I2VEC (i_o)
			pos_d = Vec2 (pos_o.x + dir.x, pos_o.y + dir.y)
			if not (0 <= pos_d.x < self.xx) or not (0 <= pos_d.y < self.yy):
				return False
			i_d = XY2I(pos_d.x, pos_d.y)
			t_d = self.tiles[i_d]
			if t_d.accessible:
				return False
			con_o = GetConnections(t_o.type, t_o.rotation)
			con_d = GetConnections(t_d.type, t_d.rotation)
			o_d = False
			d_o = False
			for con in con_o:
				if con.x == dir.x and con.y == dir.y:
					o_d = True
			for con in con_d:
				if con.x == 0-dir.x and con.y == 0-dir.y:
					d_o = True
			return o_d and d_o
		for i in range(0, self.xx*self.yy):
			self.tiles[i].accessible = False
		looseends.append (XY2I (self.sx, self.sy))
		connected = 0
		while looseends.__len__() > 0:
			i_o = looseends[0]
			looseends.remove(i_o)
			for d in [Vec2(-1,0), Vec2(0,1), Vec2(1,0), Vec2(0,-1)]:
				if IsConnectedAndValidMove(i_o, d):
					pos_o = I2VEC(i_o)
					pos_d = Vec2(pos_o.x + d.x, pos_o.y + d.y)
					i_d = XY2I(pos_d.x, pos_d.y)
					t_d = self.tiles[i_d]
					t_d.accessible = True
					looseends.append(i_d)
					connected += 1
		if connected == self.xx*self.yy:
			self.Solved = True
		else:
			self.Solved = False
			

	def Shake(self):
		"""Rotate all tiles to a random rotation"""
		for tile in self.tiles:
			tile.rotation = random.randint(0, GetRotations(tile.type)-1)

	def GetTile(self, x, y):
		"""Get Tile at location [x,y]"""
		return self.tiles[x+(y)*self.xx]
	def IsSolved (self):
		"""return (bool) "Are all tiles accessible?" """
		return self.Solved
	def Rotate (self, x, y, dir):
		"""Rotate tile at [x,y] (dir==1:CW, dir==-1:CCW, dir==0:let it be as is)"""
		tile = self.GetTile(x,y)
		tile.rotation = (tile.rotation + dir) % GetRotations(tile.type)
