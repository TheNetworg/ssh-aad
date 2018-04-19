#!/usr/bin/python
import adal
import json
from configobj import ConfigObj

context = None
config = None

# Default Constants
DEFAULT_GLOBAL_CONFIG_PATH = '/etc/ssh-aad/ssh-aad.conf'
DEFAULT_LOG_PATH = '/var/log/ssh-aad.log'

# TODO: Check permissions for VM access using ARM

def setup_adal(cnf):
    """
    Creates ADAL context.
    """
    global context
    
    context = adal.AuthenticationContext(cnf['AUTHORITY'], api_version=None)

def get_device_code(cnf):
    """
    Authenticate the end-user using device auth.
    """
    global context

    code = context.acquire_user_code('https://management.core.windows.net/', cnf['CLIENT_ID'])

    return code

def wait_for_token(code, cnf):
    global context

    token = context.acquire_token_with_device_code('https://management.core.windows.net/', code, cnf['CLIENT_ID'])

    return token

def get_local_username(pamh):
    """
    Returns the local user name wanting to authenticate
    :param pamh: PAM handle from python_pam module
    :return: local username or empty string if not found
    """
    try:
        user = pamh.get_user(None)
    except:
        user = ''

    return user

def load_config(global_config_path):
    """
    Loads the configuration from a given path
    :param global_config_path: path from where to load the configuration
    :return: object containing all the loaded configuration
    """
    global config
    config = ConfigObj(global_config_path)

    return config

def log(log_info):
    log_file = open(DEFAULT_LOG_PATH, 'a')
    log_file.writelines(log_info + '\n')
    log_file.close()

def pam_sm_authenticate(pamh, flags, argv):
    """
    pam_python implementation of the pam_sm_authenticate method of PAM modules
    This function handles and returns the authentication of a PAM module
    :param pamh: PAM handle from python_pam module
    :param flags: configuration flags given to the module
    :param argv: arguments given to the PAM module in pam.d configuration
    :return: flag indicating the success or error of the authentication
    """
    try:
        local_username = get_local_username(pamh)
        # DEBUG
        # local_username = 'hajekj'
        if local_username == '':
            return pamh.PAM_USER_UNKNOWN

        cnf = load_config(DEFAULT_GLOBAL_CONFIG_PATH)
        setup_adal(cnf)

        code = get_device_code(cnf)

        pamh.conversation(pamh.Message(4, str(code['message'])))
        pamh.conversation(pamh.Message(pamh.PAM_PROMPT_ECHO_ON, '<Press ENTER once finished>'))

        token = wait_for_token(code, cnf)

        # TODO: Parse token, create user, add to groups etc.

        if pamh is not None:
            if token is not None:
                return pamh.PAM_SUCCESS
            else:
                return pamh.PAM_USER_UNKNOWN
    except Exception as e:
        print ('Exception found:', e)
        log(str(e))

def pam_sm_setcred(pamh, flags, argv):
    return pamh.PAM_SUCCESS

def pam_sm_acct_mgmt(pamh, flags, argv):
    return pamh.PAM_SUCCESS

def pam_sm_open_session(pamh, flags, argv):
    return pamh.PAM_SUCCESS

def pam_sm_close_session(pamh, flags, argv):
    return pamh.PAM_SUCCESS

def pam_sm_chauthtok(pamh, flags, argv):
    return pamh.PAM_SUCCESS

if __name__ == "__main__":
    pam_sm_authenticate(None, None, None)
