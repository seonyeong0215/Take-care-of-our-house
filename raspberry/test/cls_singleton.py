class Cls:
	def __init__(self):
		self.vals = {'temp':0, 'bpm':0}

	def addValue(self):
		self.vals['temp'] += 1

	def getValue(self):
		return self.vals

'''
	Singleton
'''

class SingletonInstance:
	__instance = None

	@classmethod
	def __getInstance(cls):
		return cls.__instance

	@classmethod
	def instance(cls, *args, **kargs):
		cls.__instance = cls(*args, **kargs)
		cls.instance = cls.__getInstance
		return cls.__instance

class MyCls(Cls, SingletonInstance):
	pass

# vals = MyCls.instance().getValue()