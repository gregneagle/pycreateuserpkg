Tool for generating packages that create macOS user accounts on
10.8-10.15

#### NEW 12-Oct-2019:
More changes when updating existing accounts to work better with FileVault-enabled accounts. Existing authentication_authority attributes other than the ShadowHash are now preserved, and the generateduid is not changed/updated. 
This means when updating existing accounts there are three attributes that will not be changed/updated: uid, home, and generateduid. If you require these to be consistent across all machines you manage, consider _deleting_ the account before installing the new package.

#### NEW 13-Aug-2019:
The create_user.py tool in the Scripts directory of the expanded package has been replaced by a compiled createuser tool written in Objective-C. (See the createuser directory for the source). This eliminates the dependency on Apple Python for the package itself to work on the current boot volume.

#### Note:
in 10.14+ when updating an existing account, the following attributes will _NOT_ be updated: `uid` and `home`. This is due to new restrictions in Mojave.



```
$ ./createuserpkg --help
Usage: createuserpkg [options] /path/to/output.pkg

Options:
  -h, --help            show this help message and exit

  Required User Options:
    -n NAME, --name=NAME
                        User shortname. REQUIRED.
    -u UID, --uid=UID   User uid. REQUIRED.

  Required Package Options:
    -V VERSION, --version=VERSION
                        Package version number. REQUIRED.
    -i IDENTIFIER, --identifier=IDENTIFIER
                        Package identifier. REQUIRED.

  Optional User Options:
    -p PASSWORD, --password=PASSWORD
                        User password. If this is not provided, interactively
                        prompt for password.
    -f FULLNAME, --fullname=FULLNAME
                        User full name. Optional.
    -g GID, --gid=GID   User gid. Optional.
    -G GENERATEDUID, --generateduid=GENERATEDUID
                        GeneratedUID (UUID). Optional.
    -H HOME, --home=HOME
                        Path to user home directory. Optional.
    -s SHELL, --shell=SHELL
                        User shell path. Optional.
    -a, --admin         User account should be added to admin group.
    -A, --autologin     User account should automatically login.
    --hidden            User account should be hidden.

```

#### Example:

Making a local admin pkg with shortname "localadmin" and uid 501:

```
$ ./createuserpkg -n localadmin -u 501 -a -i com.foo.localadminpkg -V 1.0 localadmin.pkg
Password: ********
Password (again): ********
pkgbuild: Inferring bundle components from contents of /var/folders/tc/sd4_mtvj14jdy7cg21m2gmcw000495/T/tmpj0FQ8n/create_user
pkgbuild: Adding top-level postinstall script
pkgbuild: Wrote package to localadmin.pkg
```
