from git_dumper import fetch_git
from git_dumper import printf
from template_parser import TemplateParser
from concurrent.futures import ThreadPoolExecutor
from concurrent.futures import as_completed
from pathlib import Path 
from time import sleep
import urllib3
import sys
import re
import socket
import socks
import argparse
import os
import os.path
import helpers


# 1. Fetch everything from the target URL
# 2. Detect versions in all git files
#### a. If it is an executable file, check the version with -v or --version option

def is_fetch_succesful(folder_path):
    """Return True if given folder include a file, else return False."""

    # Get the list of files and directories in the given folder
    items = os.listdir(folder_path)

    return len(items) == 0

def main():
    parser = argparse.ArgumentParser(
        usage="git-dumper [options] URL DIR",
        description="Dump a git repository from a website.",
    )
    parser.add_argument("url", metavar="URL", help="url")
    parser.add_argument("directory", metavar="DIR", help="output directory")
    parser.add_argument("--proxy", help="use the specified proxy")
    parser.add_argument(
        "-j",
        "--jobs",
        type=int,
        default=10,
        help="number of simultaneous requests",
    )
    parser.add_argument(
        "-r",
        "--retry",
        type=int,
        default=3,
        help="number of request attempts before giving up",
    )
    parser.add_argument(
        "-t",
        "--timeout",
        type=int,
        default=3,
        help="maximum time in seconds before giving up",
    )
    parser.add_argument(
        "-u",
        "--user-agent",
        type=str,
        default="Mozilla/5.0 (Windows NT 10.0; rv:78.0) Gecko/20100101 Firefox/78.0",
        help="user-agent to use for requests",
    )
    parser.add_argument(
        "-H",
        "--header",
        type=str,
        action="append",
        help="additional http headers, e.g `NAME=VALUE`",
    )

    parser.add_argument('--vuln', action='store_true', help='Checks the vulnerabilities for dumped git files.')
    args = parser.parse_args()

    # jobs
    if args.jobs < 1:
        parser.error("invalid number of jobs, got `%d`" % args.jobs)

    # retry
    if args.retry < 1:
        parser.error("invalid number of retries, got `%d`" % args.retry)

    # timeout
    if args.timeout < 1:
        parser.error("invalid timeout, got `%d`" % args.timeout)

    # header
    http_headers = {"User-Agent": args.user_agent}
    if args.header:
        for header in args.header:
            tokens = header.split("=", maxsplit=1)
            if len(tokens) != 2:
                parser.error(
                    "http header must have the form NAME=VALUE, got `%s`"
                    % header
                )
            name, value = tokens
            http_headers[name.strip()] = value.strip()

    # proxy
    if args.proxy:
        proxy_valid = False

        for pattern, proxy_type in [
            (r"^socks5:(.*):(\d+)$", socks.PROXY_TYPE_SOCKS5),
            (r"^socks4:(.*):(\d+)$", socks.PROXY_TYPE_SOCKS4),
            (r"^http://(.*):(\d+)$", socks.PROXY_TYPE_HTTP),
            (r"^(.*):(\d+)$", socks.PROXY_TYPE_SOCKS5),
        ]:
            m = re.match(pattern, args.proxy)
            if m:
                socks.setdefaultproxy(proxy_type, m.group(1), int(m.group(2)))
                socket.socket = socks.socksocket
                proxy_valid = True
                break

        if not proxy_valid:
            parser.error("invalid proxy, got `%s`" % args.proxy)

    # output directory
    if not os.path.exists(args.directory):
        os.makedirs(args.directory)

    if not os.path.isdir(args.directory):
        parser.error("`%s` is not a directory" % args.directory)

    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    # fetch everything
    fetch_git(
            args.url,
            args.directory,
            args.jobs,
            args.retry,
            args.timeout,
            http_headers,
        )
    
    folder_path = os.getcwd()
    if not is_fetch_succesful(folder_path):
        print('[i] Fetch operation done. And .git file found successfully.')

    
    # Check for vulnerability scanning process
    if not args.vuln:
        return
    else:
        if is_fetch_succesful(folder_path):
            print('[!] Since the .git file couldn\'t fetch, vulnerability scanning process passing.\n')
            return
        else:
            print('----------------------------------------\n[i] Starting vulnerability scanning process...')
            vuln_scan(folder_path)

def vuln_scan(git_folder):
    #return 1 if vuln found 0 if not

    template_count, templates = helpers.count_files_recursive("../templates")

    printf('[-] Target: %s\n', git_folder)
    printf('[-] %s template(s) using...\n', template_count)

    target_file_count, target_files = helpers.count_files_recursive(git_folder)
    process_files_with_templates(templates, target_files)

def process_files_with_templates(templates, target_files):
    """Analyze target files concurrently using a ThreadPoolExecutor"""
    with ThreadPoolExecutor() as executor:
        future_to_template = {executor.submit(analyzer, template, target_files): template
                              for template in templates}

        for future in as_completed(future_to_template):
            template = future_to_template[future]
            future.result()
            """try:
                future.result()
            except Exception as exc:
                print(f"[!] An error occurred while analyzing template '{template}': {exc}")"""

def analyzer(template, target_files):
    """Analyzes the target_files according to the template"""

    # Analyze the target_files by using the parser
    for target_file in target_files:
        # Create the template parser for the template
        parser = TemplateParser(template)
        file_content = open(target_file, "r", encoding="latin-1").read()

        # Parser using a single regex, not a regex list
        if parser.matcher_regex != None and parser.matcher_regex_list == None:
            if parser.type == "content-checker":
                if parser.matcher(parser.matcher_regex, file_content):
                    printf('<%s>: Matched! Version identified: %s \n', parser.id, parser.extractor(parser.extractor_regex, parser.match))
        
        # Parser using a regex list, not a single regex
        elif parser.matcher_regex == None and parser.matcher_regex_list != None:
            if parser.type == "filename-checker":
                # Compare each regex with the target file
                for regex in parser.matcher_regex_list:
                    if parser.matcher(regex, target_file):
                        printf('<%s>: Matched! Found file: %s, used regex: %s\n', parser.id, target_file, regex)


        

         
    
    
if __name__ == "__main__":
    main()