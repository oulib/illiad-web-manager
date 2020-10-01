import requests
import secrets
from zipfile import ZipFile
import datetime
import os
import shutil
import sys

def pull(branch, targetDir, git_repo, user):
    # Backup Current CSS, HTML, and JS from ILLiad Web
    with ZipFile("illiad-web-backup-"+ datetime.date.today().strftime("%Y-%m-%d") +".zip", "w") as backup:
        # Iterate over all the files in directory
        for folderName, subfolders, filenames in os.walk(targetDir):
            for fileName in filenames:
                if fileName.endswith('.htm') or fileName.endswith('.html') or fileName.endswith('.css') or fileName.endswith('.js'): 
                    #create complete filepath of file in directory
                    filePath = os.path.join(folderName, fileName)
                    # Add file to zip
                    backup.write(filePath)


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
            
        latest_stamp = datetime.datetime.strptime("2000-09-22T21:51:49Z","%Y-%m-%dT%H:%M:%SZ")
        zip_url = ""
        for tag in branch_releases:
            for key,release in tag.items():
                if latest_stamp < release['published_at']:
                    tag_name = key
                    latest_stamp = release['published_at']
                    zip_url = release['zipball_url']

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
        shutil.copytree(newDir, targetDir, dirs_exist_ok=True)


if __name__ == "__main__":
    try:
        git_repo = secrets.git_repo
        user = (secrets.git_user, secrets.git_password)
        pull(sys.argv[1], secrets.testDir, git_repo, user)
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
  
        
