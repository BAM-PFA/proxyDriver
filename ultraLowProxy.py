import os
import subprocess
import sys

# INPATH SHOULD BE /PATH/TO/Video_Deliverables
# OUTPATH SHOULD BE A DIR FOR EACH PRODUCTION (WLTVS,4MY,GFA)


class Migration:
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
			outPath
			]
		output = subprocess.run(command,stdout=subprocess.PIPE)
		print(output.stdout)

	def upload()

def main(batchPath,outDir):
	for root, dirs, files in os.walk(batchPath):
		for _dir in dirs:
			for _file in os.listdir(os.path.join(root,_dir)):
				if _file.endswith('.mp4'):
					migrate = Migration(
						_file,
						os.path.join(root,_dir,_file),
						outDir
						)
					migrate.transcode()



if __name__ == "__main__":
	main(sys.argv[1],sys.argv[2])
