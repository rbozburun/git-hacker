
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
```


## Credits
The git-dumper.py script written by [@arthaud](https://github.com/arthaud). I've just added "--vuln" parameter to his script and created a new tool. Since the new tool scans also the content, I've created a new repository. You can check his repository:
- [git-dumper.py](https://github.com/arthaud/git-dumper)


