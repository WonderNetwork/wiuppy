import requests
import json

class WIU:
    URL = 'https://api.wheresitup.com/v2/'
    headers = { 'Content-Type': 'application/json' }

    def __init__(self, client, token):
        self.headers['Auth'] = 'Bearer ' \
            + self._is_valid_id(client) + ' ' \
            + self._is_valid_id(token)

    def locations(self):
        return self._get('sources')

    def submit(self, target, services, locations):
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
        return self._get('retrieve/' + self._is_valid_id(id))

    def _get(self, endpoint):
        return requests.get(self.URL + endpoint, headers=self.headers).json()

    def _post(self, endpoint, data):
        return requests.get(
            self.URL + endpoint,
            headers=self.headers,
            data=json.dumps(data)
        ).json()

    def _is_valid_id(self, id):
        int(id, 16)
        return id
