import os
import platform


def get_os_name():
    return os.name


def get_all_platform():
    return platform.uname()


def get_system():
    return platform.system()


def is_windows():
    if get_os_name() == 'nt':
        return True
    return False

#  print(get_system())
