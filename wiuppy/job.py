import json
from time import sleep

from .api import WIU

class Job:
    """
    One Where's It Up job wrapped around the WIU interface

    Attributes:
        uri:       [string] For jobs to be submitted, the URI to test
        services:  [list]   Services to be performed on the URI
        locations: [list]   WonderNetwork servers to perform services from
        results:   [dict]   For submitted jobs, the API-returned results
    """
    uri = ''
    services = []
    locations = []
    results = {}

    def __init__(self, api, id=''):
        """
        Initialize a WIU job (new or pre-existing)

        Args:
            api: [WIU] WIU instance
            id: [string] If present, the job ID for a previously-submitted job
        """
        self.id = id
        self._api = api

    @property
    def is_complete(self):
        """
        Check if the all the tasks in the current result set are complete

        Returns:
            True if all tasks are complete, else False
        """
        if not self.results:
            return False

        summary = self.results['return']['summary']
        status = [summary[location][service] for location in summary for service in summary[location]]

        return not 'in progress' in status

    def retrieve(self, poll=False):
        """
        Query the API for the current job report

        Args:
            poll: [bool] If True, queries the API once per second until the
                results are complete.
                Default: False

        Returns:
            self
        """
        self.results = self._api.retrieve(self.id)
        if not poll:
            return self

        while not self.is_complete:
            print('Polling ' + self.id)
            sleep(1)
            self.results = self._api.retrieve(self.id)

        return self

    def submit(self):
        """
        Submit the current job to the API and store the resulting job ID

        Returns:
            self
        """
        self.id = self._api.submit(self.uri, self.services, self.locations)

        return self

    def __str__(self):
        out = { 'Job ID': self.id }
        if self.results:
            out['results'] = self.results['return']['summary']

        return json.dumps(out, indent=4)

    def __repr__(self):
        return str(self)
