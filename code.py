import base64
import os
import Queue
import re
import requests
import config

from glob import glob

q = Queue.Queue()


def get(url):
    """Call the github API using personal access token."""
    conf = config.get()

    headers = {}
    if 'username' in conf['github'] and 'personal_access_token' in conf['github']:
        headers['Authorization'] = "Basic {0}".format(base64.b64encode(conf['github']['username'] + ':' + conf['github']['personal_access_token']))

    return requests.get(url, headers=headers, verify=False)


def populate_queue(src):
    """Using code from Github, create a queue of characters to use to build the image."""

    for c in src:
        content = c.replace('\n', ' ')
        try:
            content = re.sub('\s+', ' ', content).strip().encode("ascii", "ignore")
            for ch in content:
                q.put(ch)
        except:
            pass


def get_content_from_github():
    """Get the content from github."""
    conf = config.get()
    r = get(conf['github']['api_url'])
    repository_url = r.json()['repository_url'].format(owner=conf['github']['owner'], repo=conf['github']['repo'])
    r = get(repository_url)

    branches_url = r.json()['branches_url'].replace('{/branch}', '/{0}'.format(conf['github']['branch']))
    r = get(branches_url)

    master_tree_url = r.json()['commit']['commit']['tree']['url'] + '?recursive=1'
    r = get(master_tree_url)

    content = []
    for t in r.json()['tree']:
        if re.match(conf['general']['code_file_regex'], t['path']):
            r = get(t['url'])
            if 'content' in r.json():
                content.append(base64.b64decode(r.json()['content']))
    return content


def get_content_from_local():
    """Get the file content from the local source."""
    conf = config.get()
    content = []
    files = [y for x in os.walk(conf['local']['path']) for y in glob(os.path.join(x[0], '*'))]
    filtered_files = [f for f in files if re.match(conf['general']['code_file_regex'], f)]

    for f in filtered_files:
        with open(f, 'r') as file:
            content.append(file.read())

    return content


def get_char():
    """Get the next character to use for the image."""
    conf = config.get()
    if q.empty():
        content = None
        if(conf["general"]["source"] == "local"):
            content = get_content_from_local()
        else:
            content = get_content_from_github()
        populate_queue(content)

    return q.get()
