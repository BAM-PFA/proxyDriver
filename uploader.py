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

# If modifying these scopes, delete the file token.pickle.
SCOPES = [
	'https://www.googleapis.com/auth/documents',
	'https://www.googleapis.com/auth/drive',
	"https://www.googleapis.com/auth/drive.file"
	]


FILES = ['file1.txt','file2.txt','file3.txt']

def login():
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
				'secrets/credentials.json', SCOPES)
			creds = flow.run_local_server(port=0)
		# Save the credentials for the next run
		with open('secrets/token.pickle', 'wb') as token:
			pickle.dump(creds, token)

	g_drive = build('drive','v3',credentials=creds)

	return g_drive



def insert_request(insertList,service,docID):
	service.documents().batchUpdate(
		documentId=docID,
		body={'requests':insertList}
		).execute()




def main():
	g_drive = login()

	for _file in FILES:
		file_metadata = {
		'name': _file,
		'parents': [FOLDER_ID]
		}
		media = MediaFileUpload(_file,
			mimetype='text/plain',
			resumable=True)
		print(file_metadata)
		uploaded_file = g_drive.files().create(body=file_metadata,
												media_body=media,
												fields='id',
												supportsAllDrives=True).execute()
		print(uploaded_file.get('id'))

if __name__ == '__main__':
	main()