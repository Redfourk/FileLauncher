import logging


import time

print("Welcome to the FileLauncher CLI")
print("Please take some time to input some settings.")

# Verbose Log Setting:
def verbose_logs():
    show_log = input("Would you like to see the logs? (Y/N): ")
    if show_log == "Y" or show_log == "y":
        logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)
        return True
    elif show_log == "N" or show_log == "n":
        return False
    else:
        verbose_logs()
vblogs = verbose_logs()

# Check for Network:
if vblogs == bool(True):
    logging.debug('Identifying network')

from netman_cli import *
def netcheck():
    print("A network is needed to use this program and the current status on this device has been identified as " + check_adapter_status())
    netcorrect = input("Is this information correct? (Y/N): ")
    if netcorrect == "Y" or netcorrect == "y":
        return True
    elif netcorrect == "N" or netcorrect == "n":
        print("Please connect to a network or check out the repo for more information")
        exit("Network Error")
    else:
        netcheck()
net_status = netcheck()

# Sending or Recieving?
def role():
    role_type = input("Would you like to send a file or receive one? (S/R): ")
    if role_type == "S" or role_type == "s":
        return "sender"
    elif role_type == "R" or role_type == "r":
        return "receiver"
    else:
        print("Please enter a valid role")
        role()
role_type = role()

if vblogs == bool(True):
    logging.debug("Role set to " + role_type)
time.sleep(1)

# Show Selected Settings:
print(
"""
Settings:

Verbose Logs: """ + str(vblogs) + """
Network Status: """ + str(net_status) + """
Role: """ + str(role_type) + """
"""
)