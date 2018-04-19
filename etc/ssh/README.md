#Updated SSHd configuration

The two main settings that need to be updated in sshd daemon's configuration so it is compatible with CYCLONE's 
PAM module settings are:

* **PasswordAuthentication no**: this disables Password authentication and forces Keyboard-Interactive
*  **UsePAM yes**: Allows SSH to use PAM
 
Other interesting settings that could be changed are:
* **PermitRootLogin**: To enable or disable the possibility to login as root via SSH
* **PubkeyAuthentication**: To enable or disable the possibility to login using SSH-RSA key.
If enabled, Public Key will have priority before Keyboard-Authentication when logging in.