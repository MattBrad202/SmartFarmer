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
	
	def run(self, recording):
		if self.localRecording != recording:
			#ESP32-1: c8:f0:9e:4a:92:76
			#ESP32-2: c8:f0:9e:4f:dd:02
			nodePairs = {'1':'c8:f0:9e:4a:92:76', '2':'c8:f0:9e:4f:dd:02'}
			for node in nodePairs:
				nodeID = node
				nodeMAC = nodePairs[node]
				print('Attempting to connect to node ' + nodeID + '...')
				filename = getNodeDataBLE(nodeID, nodeMAC)
				uploadNodeData(nodeID, filename)
		else:
			print('Not searching for Bluetooth connection')
			
		self.localRecording = recording
		
	def shutdown(self):
		print('Shutting Down Bluetooth Part...')


