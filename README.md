# illiad-web-manager
_Management Scripts for ILLiad Web Platform backed by a Git Environment_
---

This module synchronizes ILLiad a production web platform with a release on github 

---
**Requires:**

Access to ILLiad Web Platform

Access to Web Platform Github Repository

Python 3.6+

pip

Python Packages

* [requests](https://requests.readthedocs.io/en/master/) 

  - _"Requests is an elegant and simple HTTP library for Python, built for human beings. Requests allows you to send HTTP/1.1 requests extremely easily. There’s no need to manually add query strings to your URLs, or to form-encode your POST data. Keep-alive and HTTP connection pooling are 100% automatic, thanks to urllib3."_

---
This is accomplished by:

* Pulling down the newest release of the Web Platform via Github API
* Backing up existing production Web Platform 
* Extracting the Web Platform release to the defined ILLiad Web Platform location
    - NOTE: This will overwrite existing pre-defined files based on file extenstion filters. 

The following files are expected to exist in the directory
from which this module is executed:

* secrets.py  
    - A collection of directory mappings and GitHub Authentication credentials

---

Example Usage:
```
  import os
  import requests
  import secrets.py
  

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
  
  
  
```

