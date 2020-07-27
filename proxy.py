import os
import subprocess
import sys
from uploader import Upload

class Migration:
	'''
	Instance of a migration:
	transocde a low res proxy file,
	then upload it to Drive
	'''
	def __init__(
		self,
		baseName,
		inPath,
		outDir
		):

		self.baseName = baseName
		self.inPath = inPath
		self.outDir = outDir
		self.outPath = os.path.join(outDir,baseName)

	def transcode(self):
		command = [
			"ffmpeg",
			"-i",
			self.inPath,
			"-crf",
			"24",
			"-c:v",
			"libx264",
			"-pix_fmt",
			"yuv420p",
			"-c:a",
			"aac",
			"-movflags",
			"+faststart",
			self.outPath
			]
		output = subprocess.run(command,stdout=subprocess.PIPE)
		print(output.stdout)

	def upload(self):
		uploading_file = Upload(self.outPath,self.baseName)
		uploading_file.login()
		uploading_file.upload_it()

	def delete_me(self):
		try:
			os.path.remove(self.outPath)
		except:
			print("\n\n**\n\ncouldn't delete "+self.outPath)
