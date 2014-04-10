import requests
import json

class WIU:
    """
    A wrapper for the Where's It Up API

    Attributes:
        URL:     [string] The WIU API URL
        headers: [dict]   Headers to send with API calls
    """
    URL = 'https://api.wheresitup.com/v2/'
    headers = { 'Content-Type': 'application/json' }

    def __init__(self, client, token):
        """
        Initialize an instance of the API with authentication information
        http://api.wheresitup.com/docs/v2#authentication

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
        http://api.wheresitup.com/docs/v2#cities

        Returns:
            A dict containing server details
        """
        return self._get('sources')

    def submit(self, target, services, locations):
        """
        Submit a new WIU job
        http://api.wheresitup.com/docs/v2#jobs

        Args:
            target: [string] The URI to be tested
            services: [list] Services to be performed on the URI
                See also: http://api.wheresitup.com/docs/v2#services
            locations: [list] WIU servers to perform services from

        Returns:
            A string containing the new job ID

        Raises:
            Exception: The submission failed
        """
        data = {
            'uri': target,
            'services': services,
            'sources': locations
        }
        response = self._post('submit', data)
        try:
            id = response['jobID']
        except KeyError:
            raise Exception('Submission failed: ' + response['message'])

        return id

    def retrieve(self, id):
        """
        Get the current results for an existing WIU job
        http://api.wheresitup.com/docs/v2#reports

        Args:
            id: [string] WIU job ID to query

        Returns:
            A dict containing the current (possibly incomplete) job results

        Raises:
            ValueError: The ID is invalid
        """
        return self._get('retrieve/' + self._is_valid_id(id))

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
