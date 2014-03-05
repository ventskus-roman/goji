from urlparse import urljoin, urlparse
from netrc import netrc
import json
import requests
from goji.models import Issue


class JIRAClient(object):
    def __init__(self, base_url):
        self.base_url = base_url
        self.rest_base_url = urljoin(self.base_url, '/rest/api/2/')

        hostname = urlparse(self.base_url).hostname
        hosts = netrc().hosts

        if hostname in hosts:
            self.auth = (hosts[hostname][0], hosts[hostname][2])
        else:
            print('== Hostname %s not found in .netrc.' % hostname)
            exit()

    def get_issue(self, issue_key):
        url = urljoin(self.rest_base_url, 'issue/%s' % issue_key)
        request = requests.get(url, auth=self.auth)
        return Issue.from_json(request.json())

    def comment(self, issue_key, comment):
        url = urljoin(self.rest_base_url, 'issue/%s/comment' % issue_key)
        headers = {'content-type': 'application/json'}
        payload = json.dumps({'body': comment})
        request = requests.post(url, data=payload, headers=headers,
                                auth=self.auth)
        return (request.status_code == 201) or (request.status_code == 200)

