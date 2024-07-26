#!/usr/bin/env python3
'''
generate_exclude
----------------
Author: Jake Gustafson

This script generates a root exclude list suitable for rsync's
--exclude-from option or rsnapshot.conf. It reads:
$USERPROFILE/exclude_from_backup.txt.

This script must run as the user that has that file.

For use with rsnapshot, uncomment and change the exclude_file line in
/etc/rsnapshot.conf (or /opt/rsnapshot.conf used by Poikilos machines or
scripts) as follows:

exclude_file	/opt/rsnapshot/exclude_from_backup-absolute-generated.txt

Other features:
- generates a 1.list_of_zips.txt in each directory where "*.zip" is
  excluded, as a record of which zips were excluded from the backup
  (The full path is calculated using the location of the
  exclude_from_backup.txt file).
- The current working directory can be used as the HOME directory if it
  contains exclude_from_backup.txt. This is useful such as if the
  User's directory is mounted at a special location during a drive
  recovery where only files not excluded are desired.

For further rsnapshot notes and a setup specific to Poikilos machines
and scripts such as linux-preinstall, see
linux-preinstall/doc/rsnapshot.md.

Options:
--user              Only generate the {exclude_from_backup}
                    (combined user excludes) temp file. It is still
                    generated anyway, but exit afterward in this case.

--help              Show this help screen then exit.
'''
import sys
import os
import platform

SCRIPTS_DIR = os.path.dirname(os.path.realpath(__file__))
REPO_DIR = os.path.dirname(SCRIPTS_DIR)

if os.path.isfile(os.path.join(REPO_DIR, "linuxpreinstall", "__init__.py")):
    sys.path.insert(0, REPO_DIR)

from linuxpreinstall import (
    USER_DIR_NAME,
    echo0,
    echo1,
    echo2,
    HOME,  # profile,
    PROFILES,
)

src_parts = [
    "exclude_less_from_backup.txt",  # maybe keep large downloads etc
    "exclude_more_from_backup.txt",  # exclude any reproducible & history etc
]
# ^ formerly there was only /home/owner/exclude_from_backup.txt

src_txt_name = "exclude_from_backup.txt"
# src_txt = os.path.join(HOME, src_txt_name)
src_txt = os.path.join("/tmp", src_txt_name)

def usage():
    echo0(__doc__.format(
        exclude_from_backup=src_txt,
    ))

def generate_user_exclude():
    with open(src_txt, "w") as outs:
        for in_name in src_parts:
            in_path = os.path.join(HOME, in_name)
            with open(in_path, "r") as ins:
                for line in ins:
                    if not line.strip():
                        continue
                    outs.write(line)
    return 0

dst_confs = os.path.join("/opt", "rsnapshot")
dst_txt = os.path.join(dst_confs, "exclude_from_backup-absolute-generated.txt")

enable_chown = False
try_homes = [
    os.path.realpath("."),
    os.path.join("/home", "owner")
]
if not os.path.isfile(src_txt):
    for try_home in try_homes:
        enable_chown = True
        try_txt = os.path.join(try_home, src_txt_name)
        if os.path.isfile(try_txt):
            src_txt = try_txt
            HOME = try_home
            PROFILES, USER_DIR_NAME = os.path.split(HOME)
            # ^ Override ones from the linuxpreinstall module
            echo0("* detected {}".format(try_txt))
            break
echo0('PROFILES="{}"'.format(PROFILES))
echo0('USER_DIR_NAME="{}"'.format(USER_DIR_NAME))
echo0('HOME="{}"'.format(HOME))
echo0('src_txt="{}"'.format(src_txt))

def main():
    user_only = False

    for argi in range(1, len(sys.argv)):
        arg = sys.argv[argi]
        if arg == "--user":
            user_only = True
        elif arg == "--help":
            usage()
            return 0

    generate_user_exclude()

    if user_only:
        return 0

    if not os.path.isdir(dst_confs):
        try:
            os.makedirs(dst_confs)
        except PermissionError as ex:
            echo0(str(ex))
            echo0('You must create "{}" and give "{}" the write permission.'
                  ''.format(dst_confs, os.getlogin()))
            return 1
    with open(src_txt, 'r') as ins:
        with open(dst_txt, 'w') as outs:
            for rawL in ins:
                line = rawL.strip()
                if len(line) < 1:
                    continue
                path = line
                if path.endswith("*.zip"):
                    # Leave a trail of breadcrumbs for downloads:

                    parent = os.path.join(HOME, os.path.split(path)[0])
                    # ^ OK since ignores HOME if 2nd param starts with /
                    #   but see the other join command further down
                    #   which has to check manually since adding "*"
                    list_name = "1.list_of_zips.txt"
                    list_path = os.path.join(parent, list_name)
                    if not os.path.isfile(list_path):
                        matches = []
                        for sub in os.listdir(parent):
                            # subPath = os.path.join(parent, sub)
                            if sub.lower().endswith(".zip"):
                                matches.append(sub)
                        if len(subs) > 0:
                            this_gid = None
                            this_uid = None
                            with open(list_path, 'w') as f:
                                f.write("# generated by generate_exclude.py\n")
                                for sub in subs:
                                    subPath = os.path.join(parent, sub)
                                    if this_uid is None:
                                        this_uid = os.stat(subPath).st_uid
                                    if this_gid is None:
                                        this_gid = os.stat(subPath).st_gid
                                    f.write(sub+"\n")
                            echo0('* generated "{}"'.format(list_path))
                            if enable_chown:
                                echo0("  - changing to uid={} gid={}"
                                     "".format(this_uid, this_gid))
                                if (this_uid is None) or (this_gid is None):
                                    echo0("    FAILED: no uid or gid found for the files")
                                else:
                                    os.chown(list_path, this_uid, this_gid)
                        else:
                            echo0('* skipped creating 0-length "{}"'.format(list_path))
                    else:
                        echo0('* skipped existing "{}"'.format(list_path))
                if not path.startswith(PROFILES):
                    # and (not path.startswith("/")):
                    # ^ starting with / doesn't matter since
                    #   that prevents PROFILES and * to be prepended anyway
                    #   (the check makes no difference):
                    path = os.path.join(PROFILES, "*", path)
                outs.write(path+"\n")
        echo0('* wrote "{}"'.format(dst_txt))
    return 0


if __name__ == "__main__":
    sys.exit(main())
