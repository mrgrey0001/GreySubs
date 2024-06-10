import os
import sys
import argparse
import requests
from bs4 import BeautifulSoup
from subprocess import Popen, PIPE
import shutil
BANNER = """
   _____                 _____       _         
  / ____|               / ____|     | |        
 | |  __ _ __ ___ _   _| (___  _   _| |__  ___ 
 | | |_ | '__/ _ \ | | |\___ \| | | | '_ \/ __|
 | |__| | | |  __/ |_| |____) | |_| | |_) \__ \
  \_____|_|  \___|\__, |_____/ \__,_|_.__/|___/
                   __/ |                       
                  |___/  """
# Define the arguments
parser = argparse.ArgumentParser(description='Auto Subdomain Enumeration Tool')
parser.add_argument('-d', '--domain', help='Domain to enumerate', required=True)
parser.add_argument('-e', '--engine', help='Search engine to use (bing, google, etc.)', default='bing')
parser.add_argument('-p', '--proxy', help='Proxy server to use (e.g. http://proxy_ip:proxy_port)')

# Parse the arguments
args = parser.parse_args()

# Define the search engines
search_engines = {
    'bing': 'https://www.bing.com/search?q=site:{}',
    'google': 'https://www.google.com/search?q=site:{}'
}

# Define the proxy server
proxy = args.proxy
if proxy:
    proxies = {'http': proxy, 'https': proxy}
else:
    proxies = None

# Define the subdomain enumeration function
def enumerate_subdomains(domain, engine):
    # Try to use sublist3r if it's installed
    if is_sublist3r_installed():
        return use_sublist3r(domain, engine)
    else:
        # Fallback to web scraping approach
        return use_web_scraping(domain, engine)

def is_sublist3r_installed():
    return shutil.which('sublist3r') is not None

def use_sublist3r(domain, engine):
    # Use sublist3r to enumerate subdomains
    command = f"sublist3r -d {domain} -e {engine}"
    process = Popen(command, shell=True, stdout=PIPE, stderr=PIPE)
    output, error = process.communicate()
    if process.returncode == 0:
        return list(set(output.decode('utf-8').splitlines()))
    else:
        return []

def use_web_scraping(domain, engine):
    # Use web scraping approach to enumerate subdomains
    url = search_engines[engine].format(domain)
    response = requests.get(url, proxies=proxies)
    soup = BeautifulSoup(response.content, 'html.parser')
    subdomains = set()
    for link in soup.find_all('a'):
        href = link.get('href')
        if href and href.startswith('http'):
            subdomain = href.split('/')[2]
            subdomains.add(subdomain)
    return list(subdomains)
# Print the banner
print(BANNER)

# Enumerate subdomains
subdomains = enumerate_subdomains(args.domain, args.engine)

# Print the results
if subdomains:
    print(f"Subdomains for {args.domain}:")
    for subdomain in subdomains:
        print(subdomain)
else:
    print("No subdomains found.")
