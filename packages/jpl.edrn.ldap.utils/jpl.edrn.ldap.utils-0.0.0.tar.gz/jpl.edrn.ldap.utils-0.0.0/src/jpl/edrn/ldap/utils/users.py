# encoding: utf-8

'''👩‍🔧 JPL EDRN LDAP Utilities: users.'''


from . import VERSION
from .constants import BASE_DN, OBJECT_CLASSES, PASSWORD_CORPUS, PASSWORD_LENGTH
from .logging import add_logging_arguments
from .server import add_server_arguments, get_manager_password
from passlib.hash import ldap_salted_sha1
import sys, argparse, logging, csv, ldap, ldap.modlist, base64, hashlib, random

_logger = logging.getLogger(__name__)
__version__ = VERSION


def _random_password() -> str:
    return ''.join(random.sample(PASSWORD_CORPUS, PASSWORD_LENGTH))


def create_users(connection: ldap.ldapobject.LDAPObject, csv_file, base_dn: str, replace: bool, classes: list[str]):
    _logger.debug('create_users: base_dn=%s; replace=%r; classes=%r', base_dn, replace, classes)
    for row in csv.reader(csv_file):
        uid, sn, cn, mail = row[0:4]
        if uid == 'uid':
            # Header row, skip it
            continue

        dn = f'uid={uid},{base_dn}'
        password = row[4] if len(row) > 4 else None

        if replace:
            try:
                _logger.info('%s: replace mode is on so attempting to delete it', dn)
                connection.delete_s(dn)
            except ldap.NO_SUCH_OBJECT:
                _logger.debug('Turned out there was no %s', dn)
                pass
        if not password:
            password = _random_password()
        hasher = hashlib.new('sha1', password.encode('utf-8'))
        hashed_password = '{SHA}' + base64.b64encode(hasher.digest()).decode('ascii')
        _logger.debug('Password %s is hashed to %s', password, hashed_password)
        attrs = {
            'uid': uid.encode('utf-8'),
            'sn': sn.encode('utf-8'),
            'cn': cn.encode('utf-8'),
            'mail': mail.encode('utf-8'),
            'objectClass': [i.encode('utf-8') for i in classes],
            'userPassword': hashed_password.encode('utf-8')
        }
        modlist = ldap.modlist.addModlist(attrs)
        try:
            _logger.info('%s: creating user entry', dn)
            connection.add_s(dn, modlist)
        except ldap.ALREADY_EXISTS:
            _logger.debug('Turns out %s already exists so skipping', dn)
            if replace:
                raise ValueError(f'DN {dn} already exists but we just deleted it')


def create():
    '''Entrypoint for creating users.'''
    parser = argparse.ArgumentParser(description='LDAP Utilities: create users')
    parser.add_argument('--version', action='version', version=f'%(prog)s {__version__}')
    parser.add_argument(
        'USERSFILE', nargs='?', type=argparse.FileType('r'), default=sys.stdin,
        help='CSV file containing users to add, defaults to stdin'
    )
    parser.add_argument('-r', '--replace', action='store_true', help='Replace existing users (default no)')
    parser.add_argument('-b', '--base', default=BASE_DN, help='Base distinguished name [%(default)s]')
    parser.add_argument(
        '-o', '--objectclass', nargs='*', default=OBJECT_CLASSES,
        help='Object class to apply to the user [%(default)s]'
    )
    add_logging_arguments(parser)
    add_server_arguments(parser)
    args = parser.parse_args()
    logging.basicConfig(level=args.loglevel, format='%(levelname)s %(message)s')
    _logger.debug('Initializing connection to %s', args.url)
    connection = ldap.initialize(args.url)
    password = get_manager_password(args)
    _logger.debug('Binding with manager DN %s', args.manager_dn)
    connection.simple_bind_s(args.manager_dn, password)
    create_users(connection, args.USERSFILE, args.base, args.replace, args.objectclass)
    sys.exit(0)


if __name__ == '__main__':
    create()
