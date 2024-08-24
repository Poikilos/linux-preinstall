#!/usr/bin/env python3
# formerly rsnapshot-logged.sh
import os
import shutil
import sys
import subprocess

from collections import OrderedDict
from datetime import datetime
try:
    from datetime import UTC

    def utc_now():
        return datetime.now(UTC)
except ImportError:
    # Python 2
    # scheduled for removal in future version
    def utc_now():
        return datetime.utcnow()

if __name__ == "__main__":
    SCRIPTS_DIR = os.path.dirname(os.path.realpath(__file__))
    REPO_DIR = os.path.dirname(SCRIPTS_DIR)
    sys.path.insert(0, REPO_DIR)

from linuxpreinstall.more_rsnapshot import (
    # TMTimer,
    LOG,
    LOG_NAME,
    settings,
    RSNAPSHOT_LOG,
    RSNAPSHOT_LOG_NAME,
)
from linuxpreinstall.logging2 import (
    getLogger,
)
from linuxpreinstall import (
    echo0,
)

logger = getLogger(__name__)

_, me = os.path.split(__file__)


def run_command(command):
    """Run a command and return the returncode of the process."""
    print("[{}] Running: {}".format(command, me))
    # ^ Only use stderr on error, since may be running as cron
    try:
        subprocess.check_call(command, shell=True)
        return 0  # Success
    except subprocess.CalledProcessError as e:
        return e.returncode  # Return the error code


def rsnapshot_logged(backup_type):
    if not backup_type:
        logger.error(
            "[{}] expected argument: backup type"
            " (such as alpha, beta, gamma, or delta)"
            .format(__name__),
        )
        return 1

    command = ('/usr/bin/rsnapshot -c /opt/etc/rsnapshot.conf {}'
               .format(backup_type))
    code = run_command(command)
    # Write to LOG after rsnapshot
    now = datetime.now()
    now_utc = utc_now()
    with open(LOG, 'a') as logfile:
        logfile.write("[{}]\n".format(me))
        logfile.write("# region after backup\n")
        logfile.write("last_run_utc='{}'\n".format(now_utc))
        logfile.write("last_run_local='{}'\n".format(now))

        logfile.write('last_backup_type="{}"\n'.format(backup_type))
        if code != 0:
            logfile.write('status="FAILED"\n')
            logfile.write('error={}\n'.format(code))
        else:
            logfile.write('status="OK"\n')

    # Check and copy logs
    if os.path.isdir(settings['snapshot_root']):
        dst_logs = os.path.join(settings['backup_drive'], "var", "log")
        new_settings = OrderedDict(settings)
        new_settings["dst_logs"] = dst_logs
        if not os.path.isdir(dst_logs):
            # makedirs *only* when has settings['snapshot_root']
            #   not just mountpoint:
            os.makedirs(dst_logs)
        with open(LOG, 'a') as logfile:
            logfile.write("# endregion after backup\n")
        shutil.copy(LOG, os.path.join(dst_logs, LOG_NAME))
        shutil.copy(RSNAPSHOT_LOG, os.path.join(dst_logs, RSNAPSHOT_LOG_NAME))
        if not os.path.isdir("/opt/etc"):
            os.makedirs("/opt/etc")
        commented = False
        with open("/opt/etc/rsnapshot-generated.rc") as stream:
            stream.write(
                "# Do not edit this file. It is generated on each run of {}\n"
                .format(__file__))
            # NOTE: dates are also saved to logfile (above).
            stream.write("last_run_utc='{}'\n".format(now_utc))
            stream.write(
                "last_run_utc_timestamp='{}'\n"
                .format(now_utc.timestamp()))
            stream.write("last_run_local='{}'\n".format(now))
            stream.write(
                "last_run_local_timestamp='{}'\n"
                .format(now.timestamp()))
            for k, v in new_settings.items():
                if (k not in settings) and (not commented):
                    stream.write(
                        "# runtime variables not from settings {}:\n"
                        .format(__file__))
                    commented = True
                stream.write("{}=\"{}\"\n".format(k, v))
    else:
        error = ("[{}] Error: {} is no longer mounted (no {})"
                 .format(me, settings['backup_drive'],
                         settings['rsnapshot_flag_dir']))
        with open(LOG, 'a') as logfile:
            logfile.write(error + "\n")
        logger.error(error)
        with open(LOG, 'a') as logfile:
            logfile.write("# endregion after backup\n")
        echo0("Finished writing \"{}\"".format(LOG))
        return 1

    print("Finished writing \"{}\"".format(LOG))
    # ^ Only use stderr on error, since may be running as cron
    return 0


def main():
    if len(sys.argv) != 2:
        echo0("Usage: {} <backup_type>".format(sys.argv[0]))
        sys.exit(1)
    backup_type = sys.argv[1]
    rsnapshot_logged(backup_type)


if __name__ == "__main__":
    sys.exit(main())
