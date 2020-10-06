import requests
import secrets
from zipfile import ZipFile
import datetime
import time
import os
import shutil
import sys

def pull(branch, targetDir, git_repo, user):
        # Get Releases
        repo_releases = requests.get("https://api.github.com/repos/" + git_repo+ "/tags", auth=user).json()
        branch_releases = []
        for entry in repo_releases:
            pa = ""
            zu = ""
            tn = ""
            for k,v in entry.items():
                if k == 'zipball_url':
                    zu = v
                if k == "name" and v.startswith(branch):
                    tn = v
                    pa = datetime.datetime.strptime("".join(v.split("-")[1:]),"%Y%m%d%H%M%S")
            if branch in tn:
                branch_releases.append({tn: {"published_at":pa, "zipball_url": zu}})

        latest_stamp = datetime.datetime.utcfromtimestamp(os.path.getmtime(targetDir))
        HAS_NEW_RELEASE = False
        zip_url = ""
        for tag in branch_releases:
            for key,release in tag.items():
                if latest_stamp < release['published_at']:
                    HAS_NEW_RELEASE = True
                    tag_name = key
                    latest_stamp = release['published_at']
                    zip_url = release['zipball_url']

        if HAS_NEW_RELEASE is False:
            print("No release newer than existing found for provided branch...\nexiting.")
            sys.exit(1)

        # Backup Current CSS, HTML, and JS from ILLiad Web
        with ZipFile("illiad-web-backup-"+branch+"-"+ datetime.datetime.now().strftime("%Y-%m-%d-%H%M%S") +".zip", "w") as backup:
            # Iterate over all the files in directory
            for folderName, subfolders, filenames in os.walk(targetDir):
                for fileName in filenames:
                    if fileName.endswith('.htm') or fileName.endswith('.html') or fileName.endswith('.css') or fileName.endswith('.js'): 
                        #create complete filepath of file in directory
                        filePath = os.path.join(folderName, fileName)
                        # Add file to zip
                        backup.write(filePath)


        # Initialize extracted directory var 
        newDir = ""
        if zip_url == "":
            print("No ZIP found for provided branch...\nexiting.")
            sys.exit(1)
        # Download zip of latest release
        latest_zip = requests.get(zip_url, auth=user)

        # Save latest release 
        with open(tag_name+'.zip', "wb") as file:
            file.write(latest_zip.content)


        # Extract CSS, HTML, and JS from newest release and set new directory base
        with ZipFile(tag_name+'.zip', 'r') as zipObj:
            newDir=zipObj.namelist()[0]
            for fileName in zipObj.namelist():
                if fileName.endswith('.htm') or fileName.endswith('.html') or fileName.endswith('.css') or fileName.endswith('.js'): 
                    zipObj.extract(fileName)

        # Copy extracted zip to defined ILLiad directory
        shutil.copytree(newDir+"\\htdocs", targetDir, dirs_exist_ok=True)


if __name__ == "__main__":
    try:
        git_repo = secrets.git_repo
        user = (secrets.git_user, secrets.git_password)
        backupDir = secrets.backupDir
        if sys.argv[1] == "testweb":
            pull(sys.argv[1], secrets.testDir, git_repo, user)
        if sys.argv[1] == "main":
            pull(sys.argv[1], secrets.prodDir, git_repo, user)
        if sys.argv[1].startswith("-h") or sys.argv[1].startswith("--h"):
            print("usage: pull_branch.py BRANCH_NAME")
            print("\tThis may be main/master for production instances or testweb for test branches") 
        if sys.argv[1].startswith("-h") or sys.argv[1].startswith("--h"):
            print("usage: pull_branch.py BRANCH_NAME")
            print("\tThis may be main/master for production instances or testweb for test branches")
    except AttributeError:
        print("The following vars must be defined in expected secrets file:\n")
        print("git_repo = GIT_ORG/GIT_REPO")
        print("git_user = GIT_USERNAME")
        print("git_password = GIT_PASSWORD")
        print("testDir = \"Location of ILLiad testweb directory\"\n(Typically \"C:\\inetpub\\ILLiad\\testweb\\\"\n")
        print("prodDir = \"Location of production ILLiad installation directory\"\n(Typically \"C:\\inetpub\\ILLiad\\\"")
    finally:
         for item in os.scandir('C:\\illiad-web-manager\\'):
             if item.is_dir():
                 shutil.rmtree(item.path)
             if item.name.endswith(".zip") and (item.stat().st_mtime < (time.time() - (7*86400))):
                 os.remove(item.path)
                
        
