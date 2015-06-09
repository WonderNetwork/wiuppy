import requests
import json

class WIU:
    """
    A wrapper for the Where's It Up API

    Attributes:
        URL:     [string] The WIU API entry point
        headers: [dict]   Headers to send with API calls
    """
    URL = 'https://api.wheresitup.com/v4/'
    headers = { 'Content-Type': 'application/json' }

    def __init__(self, client, token):
        """
        Initialize an instance of the API with authentication information
        http://api.wheresitup.com/docs/v4#auth

        Args:
            client: [string] WIU client ID
            token: [string] WIU client token

        Raises:
            ValueError: The client or token is invalid
        """
        self.headers['Auth'] = 'Bearer ' \
            + self._is_valid_id(client) + ' ' \
            + self._is_valid_id(token)

    def locations(self):
        """
        Get the list of available WIU servers
        http://api.wheresitup.com/docs/v4#sources

        Returns:
            A dict containing server details
        """
        return self._get('sources')

    def submit(self, target, tests, locations, options = {}):
        """
        Submit a new WIU job
        http://api.wheresitup.com/docs/v4#jobs

        Args:
            target: [string] The URI to be tested
            tests: [list] tests to be performed on the URI
                See also: http://api.wheresitup.com/docs/v4#tests
            locations: [list] WIU servers to perform tests from

        Returns:
            A string containing the new job ID

        Raises:
            Exception: The submission failed
        """
        data = {
            'uri': target,
            'tests': tests,
            'sources': locations,
            'options': options
        }

        response = self._post('jobs', data)
        try:
            id = response['jobID']
        except KeyError:
            raise Exception('Submission failed: ' + response['message'])

        return id

    def retrieve(self, id):
        """
        Get the current results for an existing WIU job
        http://api.wheresitup.com/docs/v4#reports

        Args:
            id: [string] WIU job ID to query

        Returns:
            A dict containing the current (possibly incomplete) job results

        Raises:
            ValueError: The ID is invalid
        """
        return self._get('jobs/' + self._is_valid_id(id))

    def _get(self, endpoint):
        return requests.get(self.URL + endpoint, headers=self.headers).json()

    def _post(self, endpoint, data):
        return requests.post(
            self.URL + endpoint,
            headers=self.headers,
            data=json.dumps(data)
        ).json()

    def _is_valid_id(self, id):
        int(id, 16)
        return id
