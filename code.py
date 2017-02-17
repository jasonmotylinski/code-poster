import requests
import base64
import re
import Queue
import config

q = Queue.Queue()


def get(url):
    """Call the github API using personal access token."""
    conf = config.get()

    headers = {}
    if 'username' in conf['github'] and 'personal_access_token' in conf['github']:
        headers['Authorization'] = "Basic {0}".format(base64.b64encode(conf['github']['username'] + ':' + conf['github']['personal_access_token']))

    return requests.get(url, headers=headers, verify=False)


def populate_queue():
    """Using code from Github, create a queue of characters to use to build the image."""
    conf = config.get()
    r = get(conf['github']['api_url'])
    repository_url = r.json()['repository_url'].format(owner=conf['github']['owner'], repo=conf['github']['repo'])
    r = get(repository_url)

    branches_url = r.json()['branches_url'].replace('{/branch}', '/{0}'.format(conf['github']['branch']))
    r = get(branches_url)

    master_tree_url = r.json()['commit']['commit']['tree']['url'] + '?recursive=1'
    r = get(master_tree_url)

    for t in r.json()['tree']:
        if re.match(conf['github']['code_file_regex'], t['path']):
            r = get(t['url'])
            if 'content' in r.json():
                content = base64.b64decode(r.json()['content']).replace('\n', ' ')
                try:
                    content = re.sub('\s+', ' ', content).strip().encode("ascii", "ignore")
                    for ch in content:
                        q.put(ch)
                except:
                    pass


def get_char():
    """Get the next character to use for the image."""
    if q.empty():
        populate_queue()

    return q.get()
