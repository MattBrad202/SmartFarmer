from PIL import Image
import numpy as np
import time
import sys
import subprocess
import os
from Bluetooth import *
from publish import *

class Bluetooth(object):
	def __init__(self):
		print('Ínitializing Bluetooth Part...')
		self.localRecording = False
		self.oldRecording = False
		self.running = True
		
	def run_threaded(self, recording):
		self.localRecording = recording
		
	def update(self):
		while self.running:
			self.upload()
	
	def run(self, recording):
		self.localRecording = recording
		self.upload()	
		
	def upload(self):
		time.sleep(0.1)
		if self.localRecording != self.oldRecording:
			self.oldRecording = self.localRecording
			#ESP32-1: c8:f0:9e:4a:92:76
			#ESP32-2: c8:f0:9e:4f:dd:02
			nodePairs = {'1':'c8:f0:9e:4a:92:76', '2':'c8:f0:9e:4f:dd:02'}
			for node in nodePairs:
				nodeID = node
				nodeMAC = nodePairs[node]
				print('Attempting to connect to node ' + nodeID + '...')
				try:
				    filename = getNodeDataBLE(nodeID, nodeMAC)
				    uploadNodeData(nodeID, filename)
				except Exception as e:
					print(e)
		else:
			#print('Not searching for Bluetooth connection')
			pass
		
	def shutdown(self):
		print('Shutting Down Bluetooth Part...')
		self.running = False
		time.sleep(0.2)


