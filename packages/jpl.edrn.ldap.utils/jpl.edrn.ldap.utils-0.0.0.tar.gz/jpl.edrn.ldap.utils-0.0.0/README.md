# 🏃 JPL EDRN LDAP Utilities

This package just contains some handy LDAP utilities for the [Early Detection Research Network](https://edrn.nci.nih.gov/) Directory Service. The EDRN Directory Service is an OpenLDAP-based standalone directory that also happens to handle users and groups for not just EDRN but two other consortia:

-   Consortium for Molecular and Cellular Characterization of Screen-Detected Lesions
-   National Institute of Standards and Technology


## 💽 Installation

This software requires Python 3. Python 3.9 or later is recommended, but Python 4 is not. Typically, you'll make a virtual environment and install the software with a litany like:

    python3 -m venv ldap-utils
    cd ldap-utils
    bin/pip install --upgrade --quiet setuptools wheel pip
    bin/pip install jpl.edrn.ldap.utils==X.Y.Z

where `X.Y.Z` is the version you want. To upgrade an existing installation, add `--upgrade`. Then "activate" the virtual environment (or use full paths to programs like `ldap-utils/bin/create-users`).


## 👩‍🔧 Usage

Currently the only utility is the `create-users` script, which you run as follows:

    create-users USERSFILE

where USERSFILE is a CSV file containing the users **and optionally their plain text passwords** to add to the LDAP server. For example, you'd run:

    create-users --url ldaps://naming.jpl.nasa.gov --replace newusers.csv

to add the users in `newusers.csv` to the LDAP server on `naming.jpl.nasa.gov`. If no `USERSFILE` is given, the program will read CSV data from the standard input.


### 💁‍♀️ Command-line Options

You can fine-tune the behavior of `create-users` with the following command-line options:

| Option                | Usage                                                        | Default                        |
|:----------------------|:-------------------------------------------------------------|:-------------------------------|
| `-r`, `--replace`     | If given replace existing users, overwriting all attributres | Do not replace                 |
| `-b`, `--base`        | Base DN for all users                                        | `ou=users,o=NIST`              |
| `-o`, `--objectclass` | Object classes for new users                                 | (see below)                    |
| `-h`, `--url`         | URL to LDAP server                                           | `ldaps://edrn-ds.jpl.nasa.gov` |
| `-D`, `--manager-dn`  | DN of the LDAP manager user                                  | A reasonable default           |
| `-w`, `--password`    | Password of the LDAP manager user                            | (see below)                    |

⚠️ Be careful with `-r` or `--replace`. If a user has changed their password, email address, or other attributes and their username appears in the CSV file, those changes will be lost.

In addition, you can specify either `--debug` which causes `create-users` to print verbose debugging messages during its operation or `--quiet` which causes it to only report errors. By default it gives informational messages only. You can also give `--help` to get a summary of all the command-line options, including `--version` which tells you what version you're running.


#### 🎓 Object Classes

The default object classes for users are:

-   `inetOrgPerson`
-   `organizationalPerson`
-   `person`
-   `top`

You can override this by providing `-o` or `--objectclass`; for example:

    create-users … --objectclass edrnPerson inetOrgPerson person top …


#### 🔑 LDAP Manager Password

The `create-users` program naturally needs the password for the LDAP manager so it can make updates to the user data. You can provide the password on the command line with `-w` or `--password`, but beware that other programs and users on the system will be able to see this password.

If `-w` or `--password` is not given, the password will be taken from the `MANAGER_DN_PASSWORD` environment variable. If it is empty or unset, you will be prompted for the password—which is the safest way of providing it.


### 🗂️ CSV File Format

The single CSV file expected by `create-users` should have the following columns:

| Column | Purpose                                                             | Mapped LDAP Attribute |
|-------:|:--------------------------------------------------------------------|:----------------------|
|      0 | Bare user ID (not a distinguished name), such as `joe` or `jschmoe` | `uid` (plus base DN)  |
|      1 | Surname, such as `Schmoe`                                           | `sn`                  |
|      2 | Common name, such as `Joe Schmoe`                                   | `cn`                  |
|      3 | Email address                                                       | `mail`                |
|      4 | Password, but may be blank (see below)                              | `userPassword`        |

If the first row and first column (row 0, column 0) contains the word `uid`, it's assumed to be a "header row" and is skipped. If there are additional columns beyond these five, they're ignored. Note that column 4 should contain the **plain text password** with which to create the user. However, if it's blank, then a random password will be generated for the user.

👉 **Note:** Randomly generated passwords _are not recoverable_. Those users will need to use your "forgotten password" feature (if any) to reset their passwords.

Here's an example CSV file (with header row) that describes three users, the middle one of which will get a random password:
```csv
uid,sn,cn,mail,password
joe,Schmoe,Joe Schmoe,joe@joe.com,h1ghly s3cr3t
waldo,Waldo,Where Is Waldo,waldo@waldo,com
lsimpson,Simpson,Lisa Simpson,lisa@simpsons.tv,bGdfj3z!jf01
```

## 👨‍👩‍👧‍👦 Groups

The `create-users` program does _nothing_ with LDAP groups of users. You'll have to manage those on your own. For example, you might make an LDIF file like this
```ldif
dn: cn=My Group,ou=groups,o=NIST
objectClass: groupOfUniqueNames
objectClass: top
cn: My Group
uniqueMember: uid=joe,ou=users,o=NIST
uniqueMember: uid=waldo,ou=users,o=NIST
uniqueMember: uid=lsimpson,ou=users,o=NIST
```
and use `ldapadd` to create the group.


## 🔧 Development

To develop this locally, try the following:

    git clone https://github.com/EDRN/jpl.edrn.ldap.utils
    cd jpl.edrn.ldap.utils
    python3 -m venv .venv
    .venv/bin/pip install --upgrade --silet setuptools build dist wheel
    .venv/bin/pip install --editable .
    .venv/bin/create-users …


### 👥 Contributing

You can start by looking at the [open issues](https://github.com/EDRN/jpl.edrn.ldap.utils/issues), forking the project, and submitting a pull request. You can also [contact us by email](mailto:ic-portal@jpl.nasa.gov) with suggestions.


### 🔢 Versioning

We use the [SemVer](https://semver.org/) philosophy for versioning this software. For versions available, see the [releases made](https://github.com/EDRN/jpl.edrn.ldap.sync/releases) on this project.


## 👩‍🎨 Creators

The principal developer is:

- [Sean Kelly](https://github.com/nutjob4life)


## 📃 License

The project is licensed under the [Apache version 2](LICENSE.md) license.
