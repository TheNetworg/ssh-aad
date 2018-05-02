> This is rather a Proof of Concept rather than a fully working code.

# Motivation
Managing user access to Linux machines can be very hard. For example when you have to handle SSH key distribution, remove user access etc. If your organization already uses Azure Active Directory, you can make use of this authentication plugin to be able to authenticate using Azure AD. Thanks to that, you will have all the logs in Azure AD centrally, and you can also enforce Conditional Access rules to the users.

# Setup
1. Register your application in Azure AD as a **Native** application ([tutorial](https://docs.microsoft.com/en-us/azure/active-directory/active-directory-application-proxy-native-client))
1. Set assigned access to the application ([tutorial](https://docs.microsoft.com/en-us/azure/active-directory/application-access-assignment-how-to-add-assignment))
1. Grant the application delegated permission to Azure Management API (for future needs)
1. Run following as *sudo*: `wget -O - https://raw.githubusercontent.com/thenetworg/ssh-aad/master/setup.sh | sh`
1. Configure the *AUTHORITY* and *CLIENT_ID* in `/etc/ssh-aad/ssh-aad.conf`

## Logging in
1. Perform standard SSH login except for using your UPN as username like: `ssh jan.hajek@thenetw.org@aadssh.labs.tntg.cz`
1. Your account will be created on first login, which will then fail (this is currently an unresolved bug)
1. Every other login is going to succeed (assuming you authenticate successfully)

## Accessing as sudo
If you try to enter sudo mode with AAD authenticated user, you are going to be prompted for password, which you obviously don't have. The solution is to modify `/etc/sudoers` file to allow login without password like so: `%sudo   ALL=(ALL:ALL) NOPASSWD:ALL`.

# Future
Since this is really just a PoC, this needs a lot of improvements:
- Add support for using a single client id for multiple VMs based on user's access to the machine in Azure Portal (using Azure Management API)
- Improve sudo access security - add support for enforcing MFA for initial authentication or something similar maybe
- Prevent users from adding their own SSH key for direct access

# Notes
- Tested on Ubuntu 17.10
- Heavily inspired by: https://github.com/cyclone-project/cyclone-python-pam/
