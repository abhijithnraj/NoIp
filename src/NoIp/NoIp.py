import requests

class NoIpException(Exception):
    def __init__(self,message):
        super().__init__(message)

class DynDnsStatus:
    # Source: https://www.noip.com/integrate/response 
    def __init__(self):
        status_maps = {
            0: "GOOD",
            1: "NO CHANGE",
            2: "NO HOST",
            3: "BAD AUTHENTICATION",
            4: "BAD AGEBT",
            5: "DONATOR",
            6: "ABUSE",
            7: "911"
        }
        self._status_maps = status_maps
    def statusToString(self, id):
        if(id in self._status_maps):
            return self._status_maps[id]
        return None
    @staticmethod
    def replyToStatus(response: requests.Response):
        if("good" in response.text):
            return 0
        if("nochg" in response.text):
            return 1
        if("nohost" in response.text):
            return 2
        if("badauth" in response.text):
            return 3
        if("badagent" in response.text):
            return 4
        if("!donator" in response.text):
            return 5
        if("abuse" in response.text):
            return 6
        if("911" in response.text):
            return 7
        return None

class DynDns:
    # Source: https://www.noip.com/integrate/request
    def __init__(self):
        self._url = "http://dynupdate.no-ip.com/nic/update"
        self._hostname = None
        self._username = None
        self._password = None
    def setHostName(self, hostname: str):
        self._hostname = hostname
    def setAuth(self, username: str, password: str):
        self._username = username
        self._password = password
    def update(self,ip: str):
        if((self._hostname != None) and 
           (self._username != None) and 
           (self._password != None) and
           (ip != None)):
            data = {"hostname":self._hostname,"myip":ip}
            response = requests.get(self._url, auth=(self._username,self._password) ,params=data)
            return DynDnsStatus.replyToStatus(response)
        else:
            raise NoIpException("Bad Arguments!")