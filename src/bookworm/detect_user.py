import os


def is_admin():
    if os.name == 'nt':
        try:
            # Only windows users with admin privileges can read 
            # the C:\windows\temp directory.
            temp = os.listdir(os.sep.join([os.environ.get('SystemRoot','C:\\windows'),'temp']))
        except:
            return False
        else:
            return True
    else:
        # Root has UID 0 on Unix systems.
        if 'SUDO_USER' in os.environ and os.geteuid() == 0:
            return True
        else:
            return False

