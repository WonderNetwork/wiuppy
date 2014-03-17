#!/usr/bin/env python3

import wiuppy as wiu

if __name__ == '__main__':
    import argparse
    import json

    parser = argparse.ArgumentParser(description='Make a request against the WIU API')
    parser.add_argument('-c', '--client', required=True, help="Where's It Up client ID (required)")
    parser.add_argument('-t', '--token', required=True, help="Where's It Up client token (required)")
    parser.add_argument('-u', '--uri', help='uri to query')
    parser.add_argument('-s', '--services', help='comma-separated services to run')
    parser.add_argument('-l', '--locations', help='comma-separated server locations to run from')
    parser.add_argument('-j', '--job', help='job ID for an existing request to retrieve')
    parser.add_argument('-p', '--poll', action='store_true', help='query the API until the job is complete')
    args = parser.parse_args()

    api = wiu.WIU(args.client, args.token)

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
