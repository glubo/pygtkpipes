class Configuration:
	def Defaults(self):
		self.TileSize = 30
		self.GridXX = 3
		self.GridYY = 3

	#below is singleton implementation
	class __impl:
		pass

	__instance = None

	def __init__(self):
		# Check if we already have an instance
		if Configuration.__instance is None:
			# Create and remember instance
			Configuration.__instance = Configuration.__impl()
			self.Defaults()

		# Store instance reference as the only member in the handle
		self.__dict__['_Configuration__instance'] = Configuration.__instance

	def __getattr__(self, attr):
		return getattr(self.__instance, attr)

	def __setattr__(self, attr, value):
		return setattr(self.__instance, attr, value)
