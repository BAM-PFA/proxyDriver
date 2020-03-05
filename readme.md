# Driving Ms Proxy

We needed to share a bunch of super low resolution proxy files of videos with coleagues remotely, privately, quickly, etc. Youtube was not an option, so Drive seemed like a reasonable service. I didn't want to store *another* set of derivative files for this preservation project, in part because of local storage limitations. 


## Usage

`python2 ultraLowProxy /path/to/test_videos/ /path/to/test_videos_outdir/`

The `ultraLowProxy` script expects an `inputPath` that contains one or more directories with `.mp4` files in them, and an `outputPath` where the proxy files can be stored temporarily. `other.py` expects the `FOLDER_ID` variable to be the ID (i.e., the last part of the URL, like of a Google Drive folder where you want the files stored. This should be set and changed manually as needed. 

The script then does the following:

* walks through the top-level directory 

* finding each `mp4` file, transcodes a super low res version 

  * calling `ffmpeg` via `subprocess` using the `-crf 24` flag to get a small file size that is still legible when streaming

* makes a Google Drive (v3) API call to post the file to the folder specified in `FOLDER_ID`.

* deletes the low res video file

## Setup

You need to (obv) have a Drive account, and create an API project (will add details later, just Google it), and follow the setup instructions. This project assumes you will use OAuth for authentication. When you authorize the project in the Google API dashboard, it will let you download the credentials as a JSON file. Store this in `secrets` and the first time you run the script it will launch a browser window confirming your authorization. Then the google library creates `token.pickle` which it then references on subsequent API calls. It needs to run on localhost to authenticate so if you need to run it remotely, do it on a local machine first then just `scp` the credential files to your server.

