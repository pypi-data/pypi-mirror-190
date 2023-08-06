# encoding: utf-8

'''👩‍🔧 JPL EDRN LDAP Utilities: constants.'''


import string


LDAP_SERVER     = 'ldaps://edrn-ds.jpl.nasa.gov'
BASE_DN         = 'ou=users,o=NIST'
OBJECT_CLASSES  = ['inetOrgPerson', 'organizationalPerson', 'person', 'top']
LDAP_MANAGER    = 'uid=admin,ou=system'
PASSWORD_CORPUS = string.ascii_letters + string.digits + string.punctuation
PASSWORD_LENGTH = 32
