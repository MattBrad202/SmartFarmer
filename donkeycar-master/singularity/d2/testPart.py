from PIL import Image
import numpy as np
import time
import sys
import subprocess
import os

class TakePhotoAndUploadToS3(object):
	def __init__(self):
		print('Ínitializing function for HelloWorld')
		self.localRecording = False
	
	def run(self, img_arr, recording):
		
		if img_arr is None:
			print('none')
		try:
			if self.localRecording != recording:
				BUCKET = "s3://smartfarmerbucket/"
				SRC_DIR = "/home/singularity/data"
				DEST = BUCKET + "images/"
				
				arr = np.uint8(img_arr)
				img = Image.fromarray(arr)
				filename = "/home/singularity/data/camdata_" + str(int(time.time())) + ".jpg"
				img.save(filename)
				CMD = "s3cmd put --acl-public %s %s" % (filename, DEST)
				subprocess.call(CMD, shell=True)
				os.remove(filename)
				print('Ḧello World!')
			else:
				print('Not recording')
			
		except:
			print('none')
			
		self.localRecording = recording
		
		
	def shutdown(self):
		print('Goodbye')
