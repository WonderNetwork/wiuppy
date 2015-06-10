import json
from time import sleep

from .api import WIU


class Job:
    """
    One Where's It Up job wrapped around the WIU interface

    Attributes:
        uri:       [string] For jobs to be submitted, the URI to test
        tests:     [list]   tests to be performed on the URI
        locations: [list]   WonderNetwork servers to perform tests from
        options:   [dict]   Options for the tests requested
        results:   [dict]   For submitted jobs, the API-returned results
    """
    uri = ''
    tests = []
    locations = []
    options = {}
    results = {}

    def __init__(self, api, id_=''):
        """
        Initialize a WIU job (new or pre-existing)

        Args:
            api: [WIU]    WIU instance
            id:  [string] If present, the job ID for a previously-submitted job
        """
        self.id = id_
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

        return len(self.results['response']['in_progress']) == 0

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
        while True:
            self.results = self._api.retrieve(self.id)
            if not poll or self.is_complete:
                return self

            sleep(1)
            print('Polling ' + self.id)

    def submit(self):
        """
        Submit the current job to the API and store the resulting job ID

        Returns:
            self
        """
        self.id = self._api.submit(
            self.uri,
            self.tests,
            self.locations,
            self.options
        )

        return self

    def __str__(self):
        out = {'Job ID': self.id}
        if self.results:
            out['results'] = {
                server: {
                    test: results['summary']
                    for (test, results)
                    in tests.items()
                }
                for (server, tests)
                in self.results['response']['complete'].items()
            }

        return json.dumps(out, indent=4)

    def __repr__(self):
        return str(self)
