"""
Create backup for certain date for specified channel in slack
"""
import argparse
import logging

from slack_backup import client
from slack_backup import config


def setup_logger(args):
    """Setup logger format and level"""

    level = logging.WARNING

    if args.quiet:
        level = logging.ERROR
        if args.quiet > 1:
            level = logging.CRITICAL

    if args.verbose:
        level = logging.INFO
        if args.verbose > 1:
            level = logging.DEBUG

    logging.basicConfig(level=level,
                        format="%(asctime)s %(levelname)s: %(message)s")


def generate_raport(args):
    """Generate logs"""
    slack = client.Client(args)
    slack.generate_history()


def fetch_data(args):
    """Fetch and store data"""
    slack = client.Client(args)
    slack.update()


def main():
    """Main function"""
    parser = argparse.ArgumentParser()

    subparser = parser.add_subparsers(dest='parser')
    subparser.required = True

    fetch = subparser.add_parser('fetch', help='Update local db with Slack'
                                 ' data')
    fetch.add_argument('-t', '--token', default=None, help='Slack token - '
                       'a string, which can be generated/obtained via '
                       'https://api.slack.com/docs/oauth-test-tokens page.')
    fetch.add_argument('-u', '--user', default=None, help='Username for your '
                       'Slack account')
    fetch.add_argument('-p', '--password', default=None, help='Password for '
                       'your Slack account.')
    fetch.add_argument('-e', '--team', default=None, help='Team name, which '
                       'is part of slack url, for example: if url is '
                       '"https://team.slack.com" than "team" is a name of '
                       'the team.')
    fetch.add_argument('-v', '--verbose', help='Be verbose. Adding more "v" '
                       'will increase verbosity', action="count",
                       default=None)
    fetch.add_argument('-q', '--quiet', help='Be quiet. Adding more "q" will'
                       ' decrease verbosity', action="count", default=None)
    fetch.add_argument('-c', '--channels', default=None, nargs='+',
                       help='List of channels to perform actions on. '
                       'Default is all channels.')

    fetch.add_argument('-d', '--database', default=None,
                       help='Path to the database file.')

    fetch.add_argument('-i', '--config', default=None,
                       help='Use specific config file.')

    fetch.set_defaults(func=fetch_data)

    generate = subparser.add_parser('generate', help='Generate logs out of '
                                    'data in provided database')
    generate.add_argument('-o', '--output', default=None, help="Output "
                          "directory for store logs. All logs are organised "
                          "per channel. By default it's `logs' directory")
    generate.add_argument('-f', '--format', default=None,
                          choices=('text', 'none'),
                          help='Output format. Default is none; only database '
                          'is updated by latest messages for all/selected '
                          'channels.')
    generate.add_argument('-t', '--theme', default=None,
                          choices=('plain', 'unicode'),
                          help='Choose theme for text output. It doesn\'t '
                          'affect other output formats.')

    generate.add_argument('-v', '--verbose', help='Be verbose. Adding more '
                          '"v" will increase verbosity', action="count",
                          default=None)
    generate.add_argument('-q', '--quiet', help='Be quiet. Adding more "q" '
                          'will decrease verbosity', action="count",
                          default=None)
    generate.add_argument('-c', '--channels', default=[], nargs='+',
                          help='List of channels to perform actions on. '
                          'Default is all channels.')

    generate.add_argument('-d', '--database', default=None,
                          help='Path to the database file.')

    generate.add_argument('-i', '--config', default=None,
                          help='Use specific config file.')

    generate.set_defaults(func=generate_raport)

    args = parser.parse_args()
    cfg = config.Config()
    msg = cfg.update(args)
    setup_logger(args)
    logging.info(msg)

    args.func(args)
