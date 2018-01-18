import os


def is_admin():
    """
    The function ``is_admin`` detects whether the calling process is running
    with administrator/superuser privileges. It works cross-platform on 
    either Windows NT systems or Unix-based systems.
    """
    if os.name == 'nt':
        try:
            # Only Windows users with admin privileges can read 
            # the C:\windows\temp directory.
            os.listdir(os.sep.join([os.environ.get('SystemRoot','C:\\windows'),'temp']))
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

