
# git_hacker.py
Dumps the .git folder and scans the contents of it. It uses YAML templates to scan contents of .git folder.

Using templates:
- **file-content-version-parser**: Parses the files and checks version information.
- **interesting-files**: Checks the filenames to find interesting ones.


## Install

```bash
pip install -r requirements
```


## Usage

```bash
usage: git_hacker.py URL DIR <args>

Dump a git repository from a website and scan the dumped content.

positional arguments:
URL                   url
DIR                   output directory

options:
-h, --help            show this help message and exit
--proxy PROXY         use the specified proxy
-j JOBS, --jobs JOBS  number of simultaneous requests
-r RETRY, --retry RETRY
                        number of request attempts before giving up
-t TIMEOUT, --timeout TIMEOUT
                        maximum time in seconds before giving up
-u USER_AGENT, --user-agent USER_AGENT
                        user-agent to use for requests
-H HEADER, --header HEADER
                    additional http headers, e.g `NAME=VALUE`
--vuln              Checks the vulnerabilities for dumped git files.
  
```

### Example Usage

```bash
python3 git_hacker.py http://localhost:8080 website --vuln
...
...
[-] Fetching http://localhost:8080/.git/refs/remotes/origin/ [200]
[-] Fetching http://localhost:8080/.git/logs/refs/remotes/ [200]
[-] Already downloaded http://localhost:8080/.git/refs/remotes/origin/master
[-] Fetching http://localhost:8080/.git/logs/refs/remotes/origin/ [200]
[-] Already downloaded http://localhost:8080/.git/logs/refs/remotes/origin/master
[-] Running git checkout .
Updated 0 paths from the index
[i] Fetch operation done. And .git file found successfully.
----------------------------------------
[i] Starting vulnerability scanning process...
[-] Target: C:\Users\resul\OneDrive\Desktop\Projects\git-hacker\website
[-] 2 template(s) using...
<interesting-files>: Matched! Found file: <redacted>\git-hacker\website\.bash_history, used regex: \.bash_history$
<interesting-files>: Matched! Found file: <redacted>\git-hacker\website\boot.log, used regex: \.log$
<interesting-files>: Matched! Found file: <redacted>\git-hacker\website\boot.log, used regex: boot.log
<file-content-version-parser>: Matched! Version identified: v3.7.0 - File: <redacted>\git-hacker\website\jquery.js  
<interesting-files>: Matched! Found file: <redacted>\git-hacker\website\README.txt, used regex: \.txt$
<file-content-version-parser>: Matched! Version identified:  1.2.3-alpha.something+meta-data - File: <redacted>\git-hacker\website\test2\alpha-version.txt
<interesting-files>: Matched! Found file: <redacted>\git-hacker\website\test2\alpha-version.txt, used regex: \.txt$
<file-content-version-parser>: Matched! Version identified:  1.2.3 - File: <redacted>\git-hacker\website\test2\version_test\version.yaml
<interesting-files>: Matched! Found file: <redacted>\git-hacker\website\test2\version_test\version.yaml, used regex: \.yaml$
```



## Credits
The git-dumper.py script written by [@arthaud](https://github.com/arthaud). I've just added "--vuln" parameter to his script and created a new tool. Since the new tool scans also the content, I've created a new repository. You can check his repository:
- [git-dumper.py](https://github.com/arthaud/git-dumper)


