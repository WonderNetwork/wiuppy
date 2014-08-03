## wiuppy
wiuppy is a Python3 wrapper for the
[Where's It Up API](https://api.wheresitup.com) (version 4).

### Requirements

- Python 3.2
- [`requests`](http://docs.python-requests.org/)

### Usage

See the official [Where's It Up documentation](https://api.wheresitup.com/docs)
for full API details.

#### Raw API access

```{python}
import wiuppy

# get the servers available
api = wiuppy.WIU(wiu_client_id, wiu_client_token)
print(api.locations())

# submit a new job requesting pings from Denver to www.google.com
api = wiuppy.WIU(wiu_client_id, wiu_client_token)
job_id = api.submit('http://www.google.com', [ 'ping' ], [ 'Denver' ])

# get the API response as a python dictionary
results = api.retrieve(job_id) # tasks will be 'in progress' until they complete
```

#### Access through the `Job` interface

```{python}
import wiuppy

# submit a new job and get the results
api = wiuppy.WIU(wiu_client_id, wiu_client_token)
job = wiuppy.Job(api)

job.uri = 'http://www.google.com'
job.tests = [ 'ping', 'dig', 'trace' ]
job.locations = [ 'Denver', 'Lima', 'Sydney' ]

job_id = job.submit().id # fluent interface
job.retrieve(poll=True)  # query the API until all the tasks are done

job.results # job results as a python dict
print(job)  # job result details as a formatted JSON string

# get the results from a previously submitted job
wiuppy.Job(api, job_id).retrieve()
```

#### Command-line client

For convenience, a command-line client is bundled with this project.

```
usage: wiuppy.py [-h] [-C CLIENT] [-T TOKEN] [-u URI] [-t TESTS]
                 [-l LOCATIONS] [-j JOB] [-p] [-f]

Make a request against the WIU API

optional arguments:
  -h, --help            show this help message and exit
  -C CLIENT, --client CLIENT
                        Where's It Up client ID (required)
  -T TOKEN, --token TOKEN
                        Where's It Up client token (required)
  -u URI, --uri URI     uri to query
  -t TESTS, --tests TESTS
                        comma-separated tests to run
  -l LOCATIONS, --locations LOCATIONS
                        comma-separated server locations to run from
  -j JOB, --job JOB     job ID for an existing request to retrieve
  -p, --poll            query the API until the job is complete
  -f, --findtowel
```
Run without arguments to get a list of available servers, with `-j` to get the
results from an existing job, or with `-u`/`-t`/`-l` to submit a new job.

If you'd rather not drop your WIU client and token in the command line every
time you make a request, you can use either environment variables:
```{sh}
export WIUPPY_CLIENT=abcdef
export WIUPPY_TOKEN=123456
```
or a config file at `~/.wiuppy` (`%USERPROFILE%\.wiuppy` on Windows):
```{ini}
[Auth]
client=abcdef
token=123456
```
