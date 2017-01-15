# coding=utf-8

import argparse
import logging
import os
import sys

from wfcli.tossl import WebfactionWebsiteToSsl

logger = logging.getLogger('wfcli')


def get_cli_parser():
    VERSION = '0.4'
    parser = argparse.ArgumentParser(
        "Webfaction Command Line Interface",
        description="A CLI wrapper to Webfaction APIs"
    )

    parser.add_argument("-v", "--version", action="version", version=VERSION)
    parser.add_argument('action', choices=[
        # 'install', # install redis on the server
        'secure',
        'renew',
    ],
                        help="secure: convert an http domain and all subdomain to https\n"
                             "renew: renew the https certificates",
                        )
    parser.add_argument('name',
                        nargs="?")
    parser.add_argument('--redis-password')
    parser.add_argument('--app-name')
    parser.add_argument('--webfaction-host')
    parser.add_argument('--webfaction-user')
    parser.add_argument('--webfaction-pass')
    # parser.add_argument('--force',
    #                     help="Force the renewal of certificate even if it's still valid",
    #                     default=False,
    #                     action="store_true",
    #                     )
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
    elif args.action == "renew":
        domain = args.name
        if not domain:
            print("Renew certificates for all the domains")
        else:
            print("Renew certificates for %s" % domain)
        w = WebfactionWebsiteToSsl()
        w.sync_certificates(subdomains=args.name)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(message)s")
    logging.getLogger('paramiko').setLevel(logging.WARNING)

    main()
