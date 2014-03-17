import json
from time import sleep

from .api import WIU

class Job:
    uri = ''
    services = []
    locations = []
    results = {}

    def __init__(self, api, id=''):
        self.id = id
        self._api = api

    @property
    def is_complete(self):
        if not self.results:
            return False

        summary = self.results['return']['summary']
        status = [summary[location][service] for location in summary for service in summary[location]]

        return not 'in progress' in status

    def retrieve(self, poll=False):
        self.results = self._api.retrieve(self.id)
        if not poll:
            return self

        while not self.is_complete:
            print('Polling ' + self.id)
            sleep(1)
            self.results = self._api.retrieve(self.id)

        return self

    def submit(self):
        self.id = self._api.submit(self.uri, self.services, self.locations)

        return self

    def __str__(self):
        out = { 'Job ID': self.id }
        if self.results:
            out['results'] = self.results['return']['summary']

        return json.dumps(out, indent=4)

    def __repr__(self):
        return str(self)
