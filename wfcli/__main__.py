# coding=utf-8

import argparse
import logging
import os
import sys

from wfcli.tossl import WebfactionWebsiteToSsl

logger = logging.getLogger('wfcli')


def get_cli_parser():
    VERSION = '0.1a'
    parser = argparse.ArgumentParser(
        "Webfaction Command Line Interface",
        description="A CLI wrapper to Webfaction APIs"
    )

    parser.add_argument("-v", "--version", action="version", version=VERSION)
    parser.add_argument('action', choices=[
        'install', 'secure'
    ])
    parser.add_argument('name')
    parser.add_argument('--redis-password')
    parser.add_argument('--app-name')
    parser.add_argument('--webfaction-host')
    parser.add_argument('--webfaction-user')
    parser.add_argument('--webfaction-pass')
    return parser


def main(args=None):
    """The main routine."""
    # example './cli.py install redis --app-name tambeta'
    parser = get_cli_parser()
    if args is None:
        args = sys.argv[1:]
    args = parser.parse_args(args)

    # set the credential in the environment
    if args.webfaction_user:
        os.environ['WEBFACTION_USER'] = args.webfaction_user
    if args.webfaction_pass:
        os.environ['WEBFACTION_PASS'] = args.webfaction_pass
    if args.webfaction_host:
        os.environ['WEBFACTION_HOST'] = args.webfaction_host

    if args.action == "install":
        if args.name == 'redis':
            if not args.app_name:
                print("Install Redis requires app name")
                sys.exit(1)
        else:
            print("Unknown install %s" % args.name)
    elif args.action == "secure":
        print("Converting websites in the domain %s to HTTPS" % args.name)
        w = WebfactionWebsiteToSsl()
        w.secure(domain=args.name)


if __name__ == "__main__":
    main()
