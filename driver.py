import argparse
import json
import os
import subprocess
import sys
from proxy import Migration
from uploader import Upload

def set_args():
	parser = argparse.ArgumentParser()
	parser.add_argument(
		'-m','--mode',
		choices=['proxy','upload'],
		default='proxy',
		help=(
			"Choose from:\n"
			"proxy (look for mp4 files and make proxies)\n"
			"upload (just upload existing files in the target directory"
				" declaring the mime type you want)\n"
			),
		required=True
		)
	parser.add_argument(
		'-t','--mimeType',
		default='video/mp4',
		help=("Set the mimeType you want to declare for all the files on upload.\n"
			"Default is 'mp4.' You can add more options in `mimeTypes.json` in "
			"this directory."
			),
		required=True
		)
	parser.add_argument(
		'-p','--batchPath',
		help=("Enter the full file path for the directory containing "
			"the batch you want to process."
			),
		required=True
		)
	parser.add_argument(
		'-f','--folderAlt',
		help=("Enter an alternative Drive folder ID "
			"to override the one set in `secrets/other.py`."
			)
		)
	parser.add_argument(
		'-o','--outPath',
		help=("Enter a filepath where you want the proxy "
			"files to be stored temporarily."
			)
		)

	return parser.parse_args()

def main():
	args = set_args()
	mode = args.mode
	mimeType = args.mimeType
	batchPath = args.batchPath
	folderAlt = args.folderAlt
	outPath = args.outPath

	if not mimeType == 'video/mp4':
		with open('mimetypes.json','r') as f:
			mtypes = json.load(s)
		mimeType = mtypes[mimeType]

	if mode == 'proxy':
		for root, dirs, _ in os.walk(batchPath):
			for _dir in dirs:
				for _file in os.listdir(os.path.join(root,_dir)):
					if _file.endswith('.mp4'):
						migrate = Migration(
							_file,
							os.path.join(root,_dir,_file),
							outPath
							)
						migrate.transcode()
						migrate.upload()
						migrate.delete_me()
	else:
		for _file in os.listdir(batchPath):
			filepath = os.path.join(batchPath,_file)
			mimeType = mimeType
			baseName = _file
			folderAlt = folderAlt
			loader = Upload(filepath,baseName,mimeType,folderAlt)
			
			loader.login()
			loader.upload_it() 

if __name__ == "__main__":
	main()
