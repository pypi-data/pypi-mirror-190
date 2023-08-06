# encoding: utf-8

'''👩‍🔧 JPL EDRN LDAP Utilities: logging.'''


import logging, argparse

_logger = logging.getLogger(__name__)


def add_logging_arguments(parser: argparse.ArgumentParser):
    '''Add our usual command-line logging options.'''
    group = parser.add_mutually_exclusive_group()
    group.add_argument(
        '--debug', action='store_const', dest='loglevel', const=logging.DEBUG, default=logging.INFO,
        help='🐞 Log copious and verbose messages suitable for developers'
    )
    group.add_argument(
        '--quiet', action='store_const', dest='loglevel', const=logging.WARNING,
        help="🤫 Don't log informational messages"
    )
