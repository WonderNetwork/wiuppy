import requests
import requests.exceptions
import json


class Error(Exception):
    pass


class WIU:
    """
    A wrapper for the Where's It Up API

    Attributes:
        URL:     [string] The WIU API entry point
        headers: [dict]   Headers to send with API calls
    """
    URL = 'https://api.wheresitup.com/v4/'
    headers = {'Content-Type': 'application/json'}

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

        Raises:
            Error: API communication failed
        """
        return self._get('sources')

    def submit(self, target, tests, locations, options={}):
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
            Error: API communication failed, or the submission was invalid
        """
        data = {
            'uri': target,
            'tests': tests,
            'sources': locations,
            'options': options
        }

        response = self._post('jobs', data)

        try:
            return response['jobID']
        except KeyError:
            raise Error('Submission failed: ' + response['message'])

    def retrieve(self, id_):
        """
        Get the current results for an existing WIU job
        http://api.wheresitup.com/docs/v4#reports

        Args:
            id: [string] WIU job ID to query

        Returns:
            A dict containing the current (possibly incomplete) job results

        Raises:
            ValueError: The ID is invalid
            Error: API communication failed, or the job was not found
        """
        results = self._get('jobs/' + self._is_valid_id(id_))

        if 'response' not in results:
            raise Error(results['message'])

        return results

    def _get(self, endpoint):
        try:
            return requests.get(
                self.URL + endpoint,
                headers=self.headers
            ).json()
        except requests.exceptions.RequestException as e:
            raise Error('Error talking to the API: ' + str(e))

    def _post(self, endpoint, data):
        try:
            return requests.post(
                self.URL + endpoint,
                headers=self.headers,
                data=json.dumps(data)
            ).json()
        except requests.exceptions.RequestException as e:
            raise Error('Error talking to the API: ' + str(e))

    @staticmethod
    def _is_valid_id(id_):
        int(id_, 16)
        return id_
