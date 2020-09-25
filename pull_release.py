import requests
import secrets
from zipfile import ZipFile
from datetime import date
import os
import shutil


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

# Initialize extracted directory var 
newDir = ""

# Download zip of latest release
latest_zip = requests.get(latest.json()['zipball_url'], auth=user)

# Save latest release 
with open(latest.json()['tag_name']+'.zip', "wb") as file:
    file.write(latest_zip.content)


# Extract CSS, HTML, and JS from newest release and set new directory base
with ZipFile(latest.json()['tag_name']+'.zip', 'r') as zipObj:
    newDir=zipObj.namelist()[0]
    for fileName in zipObj.namelist():
       if fileName.endswith('.htm') or fileName.endswith('.html') or fileName.endswith('.css') or fileName.endswith('.js') or 'css' in fileName: 
           zipObj.extract(fileName)

print(newDir)
# Copy extracted zip to defined ILLiad directory
shutil.copytree(newDir, dirName, dirs_exist_ok=True)

