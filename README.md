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
    - NOTE: This will overwrite existing pre-dfined files based on file extenstion filters. 

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
  

  # Get new GitHub Release
  github_release = requests.get(github_repository, auth=(git_username, git_password)
  
  
```

