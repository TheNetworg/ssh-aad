> This is rather a Proof of Concept rather than a fully working code.

# Motivation
Managing user access to Linux machines can be very hard. For example when you have to handle SSH key distribution, remove user access etc. If your organization already uses Azure Active Directory, you can make use of this authentication plugin to be able to authenticate using Azure AD. Thanks to that, you will have all the logs in Azure AD centrally, and you can also enforce Conditional Access rules to the users.

# Setup
1. Register your application in Azure AD as a **Native** application ([tutorial](https://docs.microsoft.com/en-us/azure/active-directory/active-directory-application-proxy-native-client))
1. Set assigned access to the application ([tutorial](https://docs.microsoft.com/en-us/azure/active-directory/application-access-assignment-how-to-add-assignment))
1. Grant the application delegated permission to Azure Management API (for future needs)
1. Run following as *sudo*: `wget -O - https://raw.githubusercontent.com/thenetworg/ssh-aad/master/setup.sh | sh`
1. Configure the *AUTHORITY* and *CLIENT_ID* in `/etc/ssh-aad/ssh-aad.conf`

# Future
Since this is really just a PoC, this needs a lot of improvements:
- Create dynamically user profiles, grant them rights to act as sudo
- Add support for using a single client id for multiple VMs based on user's access to the machine in Azure Portal (using Azure Management API)

# Notes
* Tested on Ubuntu 17.10
* Heavily inspired by: https://github.com/cyclone-project/cyclone-python-pam/