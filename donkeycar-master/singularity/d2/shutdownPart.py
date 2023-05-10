import os, signal

class Shutdown(object):
	def __init__(self):
		print('Ínitializing Shutdown Part...')
		self.localShutdown = False
	
	def run(self, shutdown):
		if self.localShutdown != shutdown:
			os.kill(os.getpid(), signal.SIGINT)
		
		
	def shutdown(self):
		print('Shutting Down Shutdown Part...')
