# encoding: utf-8

'''👩‍🔧 JPL EDRN LDAP Utilities: LDAP server communication.'''


from .constants import LDAP_SERVER, LDAP_MANAGER
import logging, argparse, os, getpass

_logger = logging.getLogger(__name__)


def add_server_arguments(parser: argparse.ArgumentParser):
    '''Add our usual command-line options for the LDAP server.'''
    parser.add_argument('-H', '--url', default=LDAP_SERVER, help='🔗 URL of the LDAP server [%(default)s]')
    parser.add_argument('-D', '--manager-dn', default=LDAP_MANAGER, help='🕴️ DN of the manager [%(default)s]')
    parser.add_argument(
        '-w', '--password',
        help='🔑 Password for the manager DN; defaults to MANAGER_DN_PASSWORD env var, or will be prompted if unset'
    )


def get_manager_password(options: argparse.Namespace) -> str:
    password = options.password
    if not password:
        password = os.getenv('MANAGER_DN_PASSWORD')
        if not password:
            password = getpass.getpass(f'Password for {options.manager_dn}: ')
    return password
