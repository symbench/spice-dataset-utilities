# TODO: Get the repo url
import sys
file_urls = sys.stdin

for file_url in file_urls:
    repo_url = '/'.join(file_url.split('/')[0:5])
    print(repo_url)
