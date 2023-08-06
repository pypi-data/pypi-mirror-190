import requests
import json
import os

# Define constant for the API server
API_SERVER = os.getenv('METERON_URL', 'http://localhost:8080')
TOKEN = os.getenv('METERON_TOKEN', '')


class Cluster:

    def __init__(self, token: str = '', cluster: str = '', servers: list = []):
        self.servers = servers
        self.cluster = cluster
        self.token = token

        if self.token == '':
            self.token = TOKEN

        self.headers = {
            'User-Agent': 'python-sdk/0.0.1',
            'Authorization': 'Bearer ' + self.token
        }

    def initialize(self):
        r = requests.post(f'{API_SERVER}/v1/clusters',
                          data=json.dumps({
                              'name': self.cluster,
                              'servers': self.servers,
                          }),
                          headers=self.headers)
        if r.status_code == requests.codes.ok:
            # All good
            return

        r.raise_for_status()

    def image_gen(self,
                  data: any,
                  headers: dict = {},
                  user: str = '',
                  async_request: bool = False):
        request_headers = {
            'User-Agent': self.headers['User-Agent'],
            'Authorization': self.headers['Authorization'],
            'X-Cluster': self.cluster,
            'X-User': user,
            'X-Async': str(async_request),
        }
        # Add any additional headers
        for key, value in headers.items():
            request_headers[key] = value

        r = requests.post(f'{API_SERVER}/v1/images/generations',
                          data=data,
                          headers=request_headers)
        if r.status_code == requests.codes.ok:
            # All good, return JSON
            return Result(self, r.json())

        r.raise_for_status()

    def list_image_gens(self, user: str = '', status: str = '', id: str = ''):
        params = {'user': user, 'status': status, 'id': id}
        r = requests.get(f'{API_SERVER}/v1/images/generations',
                         headers=self.headers,
                         params=params)

        if r.status_code == requests.codes.ok:
            # All good, iterate through the results and convert them into the Result
            results = []

            for image_gen_resp in r.json():
                results.append(Result(self, image_gen_resp))

            return results

        r.raise_for_status()


class Result:

    def __init__(self, cluster: Cluster, resp: dict):        
        # Cluster is required to allow for refreshing
        self.cluster = cluster
        # Persist some details about the result
        self.id = resp['id']
        self.cluster_id = resp['clusterId']
        self.user = resp['user']

        self.raw_resp = resp

    def status(self):
        return self.raw_resp['status']

    def reason(self):
        return self.raw_resp['reason']

    def refresh(self):
        """Refresh the result from the API"""
        updated = self.cluster.list_image_gens(id=self.id)
        if not updated:
            raise ValueError(f"{self.id} does not exist")
        # Update the raw response
        self.raw_resp = updated[0].raw_resp
        
    def processing(self):
        """Returns true if the result is still processing"""
        # Refresh from the API
        self.refresh()
        # Check the status
        status = self.status()
        if status == 'pending' or status == 'processing':
            return True
        return False

    def completed(self):
        status = self.status()
        if status == 'completed':
            return True
        elif status == 'pending' or status == 'processing':
            # Need to refresh results
            self.refresh()
            # Check again
            return status == 'completed'
        else:
            return False

    def failed(self):
        status = self.status()
        if status == 'failed':
            return True
        elif status == 'pending' or status == 'processing':
            # Need to refresh results
            self.refresh()
            # Check again
            return status == 'failed'
        else:
            return False

    def presigned_url(self):
        """Returns the presigned URL to the contents of the result"""
        # TODO: refresh the presigned URL if it has expired by calling the API
        # based on the ID
        if self.completed():
            return self.raw_resp['outputImages'][0]['url']
        elif self.failed():
            raise RuntimeError(f"{self.id} has failed, error: {self.raw_resp['reason']}")
        return ''        

    def load_response(self):
        """Loads the result that was returned from the inference server"""
        if self.completed():
            r = get_image_gen_result(self.raw_resp)
            # Check the status code
            if r.status_code == requests.codes.ok:
                return r

            r.raise_for_status()
        elif self.failed():
            raise RuntimeError(f"{self.id} has failed, error: {self.raw_resp['reason']}")
        return None

def get_image_gen_result(resp):
    """Retrieves the actual result from the storage service"""
    r = requests.get(resp['outputImages'][0]['url'])

    if r.status_code == requests.codes.ok:
        return r

    r.raise_for_status()