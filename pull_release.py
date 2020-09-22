import requests
import secrets
from zipfile import ZipFile
from datetime import date
import os
from os.path import basename


git_repo = secrets.git_repo
user=(secrets.git_user, secrets.git_password)
dirName = secrets.host_illiad_dir

# Backup Current CSS, HTML, and JS from ILLiad Web
with ZipFile("illiad-web-backup-"+ date.today().strftime("%Y-%m-%d") +".zip", "w") as backup:
    # Iterate over all the files in directory
   for folderName, subfolders, filenames in os.walk(dirName):
       for fileName in filenames:
           if fileName.endswith('.htm') or fileName.endswith('.html') or fileName.endswith('.css') or fileName.endswith('.js'): 
               #create complete filepath of file in directory
               filePath = os.path.join(folderName, fileName)
               # Add file to zip
               backup.write(filePath)


# Get Release
latest = requests.get("https://api.github.com/repos/" + secrets.git_repo + "/releases/latest", auth=user)

# Download zip of latest release
latest_zip = requests.get(latest.json()['zipball_url'], auth=user)

# Save latest release 
with open("newest_zip.zip", "wb") as file:
    file.write(latest_zip.content)

# Extract CSS, HTML, and JS from newest release
with ZipFile('newest_zip.zip', 'r') as zipObj:
   for fileName in zipObj.namelist():
       if fileName.endswith('.htm') or fileName.endswith('.html') or fileName.endswith('.css') or fileName.endswith('.js'): 
           zipObj.extract(fileName, 'illiad-web')


