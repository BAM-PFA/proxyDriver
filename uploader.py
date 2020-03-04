from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

import ast
import csv
import os.path
import pickle
import time

from secrets.other import FOLDER_ID

# all modified from 
# https://github.com/googleapis/google-api-python-client
# https://developers.google.com/docs/api/quickstart/python


class Upload(object):
	"""
	An Upload instance; upload a video to the Drive folder
	specified in secrets.other.FOLDER_ID
	"""
	def __init__(self, localPath,baseName):
		self.localPath = localPath
		self.baseName = baseName
		## DRIVE OAUTH SCOPES
		# If modifying these scopes, delete the file token.pickle.
		# These OAuth scopes are defined here:
		# https://developers.google.com/identity/protocols/googlescopes#drivev3
		self.SCOPES = [
			'https://www.googleapis.com/auth/documents',
			'https://www.googleapis.com/auth/drive',
			"https://www.googleapis.com/auth/drive.file"
			]
		self.g_drive = None

	def login(self):
		# Do some login stuff
		# Return live services for Docs and Drive APIs
		creds = None

		if os.path.exists('secrets/token.pickle'):
			with open('secrets/token.pickle', 'rb') as token:
				creds = pickle.load(token)
		# If there are no (valid) credentials available, let the user log in.
		if not creds or not creds.valid:
			if creds and creds.expired and creds.refresh_token:
				creds.refresh(Request())
			else:
				flow = InstalledAppFlow.from_client_secrets_file(
					'secrets/credentials.json', self.SCOPES)
				creds = flow.run_local_server(port=0)
			# Save the credentials for the next run
			with open('secrets/token.pickle', 'wb') as token:
				pickle.dump(creds, token)

		try:
			self.g_drive = build('drive','v3',credentials=creds)
		except:
			print("LOGIN ERROR")

	def upload_it(self):
		file_metadata = {
			'name': self.baseName,
			'parents': [FOLDER_ID]
			}
		media = MediaFileUpload(
			self.localPath,
			mimetype='video/mp4',
			resumable=True)
		print(file_metadata)
		
		uploaded_file = self.g_drive.files().create(
			body=file_metadata,
			media_body=media,
			fields='id',
			supportsAllDrives=True
			).execute()

		print(uploaded_file.get('id'))
