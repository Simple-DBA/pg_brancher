import time
import multiprocessing
import os
import yaml

def daemon_proc():
    while True:
        print("Daemon process is running")
        time.sleep(1)

def load_lockfile_path(config_file):
    with open(config_file, 'r') as f:
        config = yaml.safe_load(f)
        lockfile_path = config.get('daemon_config', {}).get('lockfile_path')
    return lockfile_path

def create_lockfile():
    lockfile_path = load_lockfile_path()
    if not lockfile_path:
        print("Lockfile path is not defined in the config file.")
        exit(1)

    pid = str(os.getpid())
    if os.path.exists(lockfile_path):
        print("Daemon is already running.")
        exit(1)
    else:
        with open(lockfile_path, 'w') as lockfile:
            lockfile.write(pid)
        print("Daemon started. PID:", pid)

def delete_lockfile():
    lockfile_path = load_lockfile_path()
    if not lockfile_path:
        print("Lockfile path is not defined in the config file.")
        exit(1)

    os.remove(lockfile_path)
    print("Daemon stopped.")

