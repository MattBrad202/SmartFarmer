from PIL import Image
import numpy as np
import time
import sys
import subprocess
import os

class TakePhotoAndUploadToS3(object):
	def __init__(self):
		print('Ínitializing Photo Capture Part...')
		self.localRecording = False
		self.running = True
		self.oldRecording = False
		self.img_arr = None
	
	def run_threaded(self, img_arr, recording):
		self.img_arr = img_arr
		self.localRecording = recording
			
	def update(self):
		while self.running:
			self.upload()
	
	def run(self, img_arr, recording):	
		self.img_arr = img_arr
		self.localRecording = recording
		self.upload()
		
	def upload(self):
		time.sleep(0.1)
		if self.img_arr is None:
			#print('none')
			pass
		try:
			if self.localRecording != self.oldRecording:
				self.oldRecording = self.localRecording
				BUCKET = "s3://smartfarmerbucket/"
				SRC_DIR = "/home/singularity/data"
				DEST = BUCKET + "images/"
				
				arr = np.uint8(self.img_arr)
				img = Image.fromarray(arr)
				filename = "/home/singularity/data/camdata_" + str(int(time.time())) + ".jpg"
				img.save(filename)
				CMD = "s3cmd put --acl-public %s %s" % (filename, DEST)
				subprocess.call(CMD, shell=True)
				os.remove(filename)
				#print('Ḧello World!')
			else:
				#print(self.localRecording, self.oldRecording)
				pass
			
		except Exception as e:
			print(e)
			
		
		
	def shutdown(self):
		print('Shutting Down Photo Capture Part...')
		self.running = False
		time.sleep(0.2)
