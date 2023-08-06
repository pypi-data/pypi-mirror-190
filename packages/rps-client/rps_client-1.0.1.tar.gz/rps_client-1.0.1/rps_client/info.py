import os
import platform
import socket


def get_hostname():
    return socket.gethostname()


def get_user_home():
    return os.path.expanduser("~")


def get_user_dir():
    return os.path.expanduser("~")


def get_python_version():
    return os.sys.version


def get_python_version_info():
    return os.sys.version_info


def get_os_name():
    return platform.system()


def get_os_uname() -> os.uname_result:
    return platform.uname()


def get_os_version():
    return platform.release()
