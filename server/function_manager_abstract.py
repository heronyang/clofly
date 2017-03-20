from abc import ABCMeta, abstractmethod

class FunctionManagerAbstract:

	__metaclass__ = ABCMeta

	@abstractmethod
	def load(self):
		pass

	@abstractmethod
	def run(self):
		pass

	@abstractmethod
	def stop(self):
		pass
