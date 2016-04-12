import os

def is_admin():
    # On *nix systems.
    return os.geteuid() == 0