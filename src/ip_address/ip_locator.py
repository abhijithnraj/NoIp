import abc
from utils.request_handler import RequestHandler
import json

class ISPDetectionStrategy(abc.ABC):

    def __init__(self,url:str,ip:str=None):
        self.url = url
        self.ip = ip
    def setIp(self,ip:str):
        self.ip=ip
    # Define an abstract method to get the IP address
    @abc.abstractmethod
    def get_provider(self):
        pass

class RequestsStrategy(ISPDetectionStrategy):
    def __init__(self,url:str,ip:str=""):
        super().__init__(url,ip)
    
    def get_provider(self):
        # Create a request handler object with the URL
        request_handler = RequestHandler(self.url)
        # Send the request and get the response
        response = request_handler.send_request()

        return response.text


class IPAPIStrategy(RequestsStrategy):
    def __init__(self,ip:str=""):
        url = f"http://ip-api.com/json/{ip}?fields=query,isp"
        super().__init__(url,ip)

    def get_provider(self):
        response = super().get_provider()
        if response :
            response  = json.loads(response)
            assert("query" in response)
            assert("isp" in response)
            self.ip = response["query"]
            return response["isp"]

class ISPDetector:
    def __init__(self,strategy:ISPDetectionStrategy,ip:str=""):
        self.strategy = strategy
        self.ip = ip
        self.provider = None
    def set_strategy(self,strategy):
        self.strategy = strategy 

    def get_provider(self):
        self.provider = self.strategy.get_provider()
        if(not self.ip):
            self.ip = self.strategy.ip
            return self.provider 
        
    def get_ip(self):
        return self.ip

if __name__=="__main__":
    isp_detector = ISPDetector(IPAPIStrategy())
    print(isp_detector.get_provider())
    print(isp_detector.get_ip())

