import os

SUPER_USER_ID = 0

def is_admin():
    # Root has UID 0 on Unix systems.
    return os.geteuid() == SUPER_USER_ID