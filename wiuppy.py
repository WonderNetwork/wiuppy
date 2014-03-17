#!/usr/bin/env python3

import wiuppy as wiu

if __name__ == '__main__':
    import argparse, json, os, configparser

    # look for auth information in the environment
    client, token = None, None
    if 'WIUPPY_CLIENT' in os.environ:
        client = os.environ['WIUPPY_CLIENT']
    if 'WIUPPY_TOKEN' in os.environ:
        token = os.environ['WIUPPY_TOKEN']

    # look for auth information in a config file
    config = configparser.ConfigParser()
    if config.read([os.path.join(os.path.expanduser('~'), '.wiuppy')]):
        client = config['Auth'].get('client', client)
        token = config['Auth'].get('token', token)

    parser = argparse.ArgumentParser(description='Make a request against the WIU API')
    parser.add_argument('-c', '--client', required=not bool(client), help="Where's It Up client ID (required)")
    parser.add_argument('-t', '--token', required=not bool(token), help="Where's It Up client token (required)")
    parser.add_argument('-u', '--uri', help='uri to query')
    parser.add_argument('-s', '--services', help='comma-separated services to run')
    parser.add_argument('-l', '--locations', help='comma-separated server locations to run from')
    parser.add_argument('-j', '--job', help='job ID for an existing request to retrieve')
    parser.add_argument('-p', '--poll', action='store_true', help='query the API until the job is complete')
    args = parser.parse_args()

    # set up the api using auth information from the environment, config file,
    # or command-line
    client = args.client or client
    token = args.token or token
    api = wiu.WIU(client, token)

    # if a job id is specified, retrieve it
    if args.job:
        job = wiu.Job(api, args.job)
        print(job.retrieve(args.poll))

        exit()

    # if a new job is requested, submit it and get the id
    if args.uri and args.services and args.locations:
        job = wiu.Job(api)

        job.uri = args.uri
        job.services = args.services.split(',')
        job.locations = args.locations.split(',')
        job.submit()

        if args.poll:
            print(job.retrieve(args.poll))
        else:
            print(job)

        exit()

    # with no arguments, print the server list
    print(json.dumps(api.locations(), indent=4))
