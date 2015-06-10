#!/usr/bin/env python3

import wiuppy as wiu


def add_option(options, raw):
    names, value = raw.split('=', 2)
    names = names.split(':')

    if value.isdigit():
        value = int(value)

    o = options
    last = len(names) - 1
    for idx, name in enumerate(names):
        val = value if idx == last else {}
        o = o.setdefault(name, val)


if __name__ == '__main__':
    import argparse
    import json
    import os
    import configparser

    client, token = None, None

    # look for auth information in a config file
    config = configparser.ConfigParser()
    if config.read([os.path.join(os.path.expanduser('~'), '.wiuppy')]):
        client = config['Auth'].get('client', client)
        token = config['Auth'].get('token', token)

    # look for auth information in the environment
    if 'WIUPPY_CLIENT' in os.environ:
        client = os.environ['WIUPPY_CLIENT']
    if 'WIUPPY_TOKEN' in os.environ:
        token = os.environ['WIUPPY_TOKEN']

    parser = argparse.ArgumentParser(
        description='Make a request against the WIU API'
    )
    parser.add_argument(
        '-C',
        '--client',
        required=not bool(client),
        help="Where's It Up client ID (required)"
    )
    parser.add_argument(
        '-T',
        '--token',
        required=not bool(token),
        help="Where's It Up client token (required)"
    )
    parser.add_argument('-u', '--uri', help='uri to query')
    parser.add_argument('-t', '--tests', help='comma-separated tests to run')
    parser.add_argument(
        '-l',
        '--locations',
        help='comma-separated server locations to run from'
    )
    parser.add_argument(
        '-j',
        '--job',
        help='job ID for an existing request to retrieve'
    )
    parser.add_argument(
        '-p',
        '--poll',
        action='store_true',
        help='query the API until the job is complete')

    parser.add_argument(
        '-o',
        '--option',
        action='append',
        help='set an option for a test as <test>:<option>=<value>, e.g.  nametime:nameserver=8.8.8.8'
    )
    args = parser.parse_args()

    # set up the api using auth information from the environment, config file,
    # or command-line
    client = args.client or client
    token = args.token or token
    api = wiu.WIU(client, token)

    # if a job id is specified, retrieve it
    if args.job:
        job = wiu.Job(api, args.job)

        try:
            print(job.retrieve(args.poll))
        except wiu.Error as e:
            print(e)

        exit()

    # if a new job is requested, submit it and get the id
    if args.uri and args.tests and args.locations:
        job = wiu.Job(api)

        job.uri = args.uri
        job.tests = args.tests.split(',')
        job.locations = args.locations.split(',')
        job.options = {}

        if args.option:
            [add_option(job.options, o) for o in args.option]

        try:
            job.submit()
        except wiu.Error as e:
            print(e)
            exit()

        if args.poll:
            try:
                print(job.retrieve(args.poll))
            except wiu.Error as e:
                print(e)
        else:
            print(job)

        exit()

    # with no arguments, print the server list
    try:
        print(json.dumps(
            [server['name'] for server in api.locations()['sources']]))
    except wiu.Error as e:
        print(e)
