# Proxy Driver

We needed to share a bunch of super low resolution proxy files of videos with coleagues remotely, privately, quickly, etc. Youtube was not an option, so Drive seemed like a reasonable service. I didn't want to store *another* set of derivative files for this preservation project, in part because of local storage limitations.

Updated to also allow for uploading existing files to a specified Drive folder without making proxies.

## Usage

`python3 driver.py` `-mode [proxy/upload]` `-mimeType [default=mp4]` `-batchPath /path/to/dir/with/files/` `-outpath /path/to/output/dir/` `[-folderAlt optional alternative Drive folder ID]`

The `driver` script can be run in either `proxy` or `upload` mode:

### In `proxy` mode, it does the following:

* expects an `batchPath` that contains one or more directories with `.mp4` files in them, and an `outPath` where the proxy files can be stored temporarily.

* `walks` through the top-level batchPath directory

* finding each `mp4` file, transcodes a super low res version

  * calling `ffmpeg` via `subprocess` using the `-crf 24` flag to get a small file size that is still legible when streaming

* makes a Google Drive (v3) API call to post the file to the folder specified in `FOLDER_ID` within `secrets/other.py`

* deletes the low res video file from the local machine

### In `upload` mode, it does this:

* uploads files within the specified batch directory (files must all be at the same directory level) to the Drive folder specified in `FODLER_ID` or with the command line argument `folderAlt`.

### other.py / Folder ID

`other.py` expects the `FOLDER_ID` variable to be the ID (i.e., the last part of the URL, like of a Google Drive folder where you want the files stored. This should be set and changed manually as needed.

The Drive folder ID is just the last string of characters in the folder URL, eg:

drive.google.com/drive/u/0/folders/**1FhX4a4LroLPkvnJ0woU326o3k5AtmPG9**

(You can also specify an alternative Drive folder ID when you run the script, using the argument `-folderAlt`)

### mimeTypes

You can declare mimeType values you might want to use in `mimeTypes.json`. This value is declared to Google when you want to upload the file. The default is `mp4` so if you are uploading something else you should modify this file accordingly.

## Setup

Installing the client is described pretty comprehensively on the Google API [site](https://developers.google.com/docs/api/quickstart/python).

You need to (obv) have a Drive account, and create an API "project" (will add details later, the Google instructions are pretty good), and follow the setup instructions. This project assumes you will use OAuth for authentication (it's mostly automated).

When you authorize the project in the Google API dashboard, it will let you download the credentials as a JSON file. Store this in the `secrets/` folder and the first time you run the script it will launch a browser window confirming your authorization. Then the google python client automatically creates a `token.pickle` file which it then references on subsequent API calls.

**Note:** This step that uses a browser window needs to run on a local computer to authenticate! If you need to run the project remotely, do the setup on a local machine first then just copy over the credential files to your remote computer.
