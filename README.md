Tool for generating packages that create macOS user accounts on
10.8-10.14

Note: in 10.14 when updating an existing account, the following attributes will _NOT_ be updated: `uid` and `home`. This is due to new restrictions in Mojave.


```
$ ./createuserpkg --help
Usage: createuserpkg [options] /path/to/output.pkg

Options:
  -h, --help            show this help message and exit

  User Options:
    -n NAME, --name=NAME
                        User shortname. Required.
    -u UID, --uid=UID   User uid. Required.
    -p PASSWORD, --password=PASSWORD
                        User password. Required.
    -f FULLNAME, --fullname=FULLNAME
                        User full name. Optional.
    -g GID, --gid=GID   User gid. Optional.
    -H HOME, --home=HOME
                        Path to user home directory. Optional.
    -s SHELL, --shell=SHELL
                        User shell path. Optional.
    -a, --admin         User account should be added to admin group.
    -A, --autologin     User account should automatically login.

  Package Options:
    -V VERSION, --version=VERSION
                        Package version number. Required.
    -i IDENTIFIER, --identifier=IDENTIFIER
                        Package identifier. Required.

```
