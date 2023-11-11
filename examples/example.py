import sys
try:
    from NoIp import NoIp
except ModuleNotFoundError:
    print("NoIp not found, install it by using pip install 'https://github.com/ABHIRAMSHIBU/NoIp/archive/refs/heads/develop.zip'")
    sys.exit(-1)

hostname = input("Enter your hostname:")
username = input("Enter your username:")
password = input("Enter your password:")
ipaddres = input("Enter the ip address you like to change it to:")

dynDns = NoIp.DynDns()
dynDns.setHostName(hostname)
dynDns.setAuth(username,password)
status = dynDns.update(ipaddres)

if(status == 0):
    print("Success!")
else:
    dynDnsStatus = NoIp.DynDnsStatus()
    print(dynDnsStatus.statusToString(status))