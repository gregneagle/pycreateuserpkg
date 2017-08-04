Work in progress for generating packages that create macOS user accounts on
10.8-10.13

```
$ ./createuserpkg --help
Usage: createuserpkg [options] /path/to/output.pkg

Options:
  -h, --help            show this help message and exit

  Required User Options:
    -n NAME, --name=NAME
                        User shortname. REQUIRED.
    -u UID, --uid=UID   User uid. REQUIRED.
    -p PASSWORD, --password=PASSWORD
                        User password. REQUIRED.

  Required Package Options:
    -V VERSION, --version=VERSION
                        Package version number. REQUIRED.
    -i IDENTIFIER, --identifier=IDENTIFIER
                        Package identifier. REQUIRED.

  Optional User Options:
    -f FULLNAME, --fullname=FULLNAME
                        User full name. Optional.
    -g GID, --gid=GID   User gid. Optional.
    -H HOME, --home=HOME
                        Path to user home directory. Optional.
    -s SHELL, --shell=SHELL
                        User shell path. Optional.
    -a, --admin         User account should be added to admin group.
    -A, --autologin     User account should automatically login.


```
