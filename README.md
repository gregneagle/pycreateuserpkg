Tool for generating packages that create macOS user accounts on
10.8-12.x

## macOS and Python notes

pycreateuserpkg requires Python and PyObjC. It also uses several command-line tools available on macOS. There is no support for running it on Windows or Linux.

In macOS 12.3, Apple removed the Python 2.7 install. Out-of-the-box, there is no Python installed. You'll need to provide your own Python and PyObjC to use pycreateuserpkg. It should run under Python 2.7, and Python 3.6-3.9 without issue.

Some options for providing an appropriate Python:

1) If you also use Munki, use Munki's bundled Python, available at /usr/local/munki/munki-python
2) Install Python from macadmins-python (https://github.com/macadmins/python).
3) Install Python from https://www.python.org.
5) There are other ways to install Python, inlcuding Homebrew (https://brew.sh), my relocatable-python tool (https://github.com/gregneagle/relocatable-python), using the python3 bundled with Xcode, and more.
6) Notably, if you don't use options 1 or 2 above, and install Python some other way, you'll also need to install PyObjC.

You might ask "Why not change the shebang to `#!/usr/bin/env python3` or even `#!/usr/bin/python3`? That could break many current users of the tool who _haven't_ upgraded to macOS 12.3 and don't have Xcode and/or the Command line development tools installed. If/when you upgrade to macOS 12.3, you'll need to take some action anyway. No need to punish everyone else.

#### NEW 13-March-2022:
- Due to the removal of Python 2 in macOS 12.3, the tool has been updated for compatibility with Python 3. There is still a dependency on PyObjC for plist writing, so this won't work out-of-the-box with the Python 3 installed as part of Xcode or the Command Line Development Tools (as these do not include PyObjC). This tool will work with Munki's Python, autopkg's Python, or the MacAdmins Python.
- Extensive testing has not been done under Python 3; it's possible there are new bugs caused by the changes. Please create issues for any new bugs discovered.
- "createuserpkg" renamed to "createuserpkg.py" and shebang line removed. Call the tool with the desired Python: for example `munki-python createuserpkg.py [options]`

#### NEW 12-Oct-2019:
More changes when updating existing accounts to work better with FileVault-enabled accounts. Existing authentication_authority attributes other than the ShadowHash are now preserved, and the generateduid is not changed/updated. 
This means when updating existing accounts there are three attributes that will not be changed/updated: uid, home, and generateduid. If you require these to be consistent across all machines you manage, consider _deleting_ the account before installing the new package.

#### NEW 13-Aug-2019:
The create_user.py tool in the Scripts directory of the expanded package has been replaced by a compiled createuser tool written in Objective-C. (See the createuser directory for the source). This eliminates the dependency on Apple Python for the package itself to work on the current boot volume.

#### Note:
in 10.14+ when updating an existing account, the following attributes will _NOT_ be updated: `uid` and `home`. This is due to new restrictions in Mojave.



```
$ python ./createuserpkg --help
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

  Optional Package Options:
    -d, --distribution  Creates a distribution-style package for use with
                        startosinstall
```

#### Example:

Making a local admin pkg with shortname "localadmin" and uid 501:

```
$ python ./createuserpkg -n localadmin -u 501 -a -i com.foo.localadminpkg -V 1.0 localadmin.pkg
Password: ********
Password (again): ********
pkgbuild: Inferring bundle components from contents of /var/folders/tc/sd4_mtvj14jdy7cg21m2gmcw000495/T/tmpj0FQ8n/create_user
pkgbuild: Adding top-level postinstall script
pkgbuild: Wrote package to localadmin.pkg
```
