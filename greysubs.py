import os
import sys
import argparse
import requests
from bs4 import BeautifulSoup

# Define the banner
BANNER = """

   _____                 _____       _         
  / ____|               / ____|     | |        
 | |  __ _ __ ___ _   _| (___  _   _| |__  ___ 
 | | |_ | '__/ _ \ | | |\___ \| | | | '_ \/ __|
 | |__| | | |  __/ |_| |____) | |_| | |_) \__ \
  \_____|_|  \___|\__, |_____/ \__,_|_.__/|___/
                   __/ |                       
                  |___/                        

"""

# Define the arguments
parser = argparse.ArgumentParser(description='GreySubs - Auto Subdomain Enumeration Tool')
parser.add_argument('-d', '--domain', help='Domain to enumerate', required=True)
parser.add_argument('-e', '--engine', help='Search engine to use (bing, google, etc.)', default='bing')

# Parse the arguments
args = parser.parse_args()

# Define the search engines
search_engines = {
    'bing': 'https://www.bing.com/search?q=site:{}',
    'google': 'https://www.google.com/search?q=site:{}'
}

# Define the subdomain enumeration function
def enumerate_subdomains(domain, engine):
    # Try to use sublist3r if it's installed
    if is_sublist3r_installed():
        return use_sublist3r(domain, engine)
    else:
        # Fallback to web scraping approach
        return use_web_scraping(domain, engine)

def is_sublist3r_installed():
    try:
        Popen(["sublist3r", "--version"], stdout=PIPE, stderr=PIPE).communicate()
        return True
    except OSError:
        return False

def use_sublist3r(domain, engine):
    # Use sublist3r to enumerate subdomains
    command = f"sublist3r -d {domain} -e {engine}"
    process = Popen(command, shell=True, stdout=PIPE, stderr=PIPE)
    output, error = process.communicate()
    if process.returncode == 0:
        return output.decode('utf-8').splitlines()
    else:
        return []

def use_web_scraping(domain, engine):
    # Use web scraping approach to enumerate subdomains
    url = search_engines[engine].format(domain)
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    subdomains = []
    for link in soup.find_all('a'):
        href = link.get('href')
        if href and href.startswith('http'):
            subdomain = href.split('/')[2]
            if subdomain not in subdomains:
                subdomains.append(subdomain)
    return subdomains

# Print the banner
print(BANNER)

# Enumerate subdomains
subdomains = enumerate_subdomains(args.domain, args.engine)

# Print the results
if subdomains:
    print(f"Total Unique Subdomains Found: {len(subdomains)}")
    for subdomain in subdomains:
        print(subdomain)
else:
    print("No subdomains found.")