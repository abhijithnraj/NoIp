# Import the required modules
import socket
import requests
import abc

# from utils.request_handler import RequestHandler


# Define a class for the request handler
class RequestHandler:

    # Initialize the request handler with a URL
    def __init__(self, url):
        self.url = url

    # Define a method to send the request and get the response
    def send_request(self):
        # Try to make an HTTP request to the URL using the requests module
        try:
            response = requests.get(self.url)
            # Check if the response status code is 200 (OK)
            if response.status_code == 200:
                # Return the response object
                return response
            else:
                # Raise an exception if the response status code is not 200
                raise Exception(f"Request failed with status code {response.status_code}")
        # Catch any requests exceptions
        except requests.exceptions.RequestException as e:
            # Print the error message
            print(f"Request error: {e}")
            # Return None
            return None
        # Catch any other exceptions
        except Exception as e:
            # Print the error message
            print(f"Other error: {e}")
            # Return None
            return None

# FIXME :  Add asynchronous methods 
# Define an abstract base class for the IP finder strategies
class IPFinderStrategy(abc.ABC):

    # Define an abstract method to get the IP address
    @abc.abstractmethod
    def get_ip_address(self):
        pass


# FIXME : Socket Strategy currently return 127.0.0.1
# Define a concrete class for the socket strategy
class SocketStrategy(IPFinderStrategy):

    # Override the get_ip_address method
    def get_ip_address(self):
        # Get the hostname and the IP address using the socket module
        hostname = socket.gethostname()
        ip_address = socket.gethostbyname(hostname)
        # Return the IP address
        return ip_address




# Define an abstract class for the requests strategy
class RequestsStrategy(IPFinderStrategy):

    # Initialize the requests strategy with a URL
    def __init__(self, url):
        self.url = url

    # Override the get_ip_address method
    def get_ip_address(self):
        # Create a request handler object with the URL
        request_handler = RequestHandler(self.url)
        # Send the request and get the response
        response = request_handler.send_request()
        # Check if the response is not None
        if response is not None:
            # Parse the response to get the IP address
            # This may vary depending on the strategy and the response format
            # Here we assume the response is a plain text with the IP address
            ip_address = response.text
            # Return the IP address
            return ip_address
        else:
            # Return None if the response is None
            return None

# Define a concrete class for the IPIFY requests strategy
class IPIFYRequestsStrategy(RequestsStrategy):

    # Initialize the IPIFY requests strategy with the IPIFY URL
    def __init__(self):
        super().__init__("https://api.ipify.org")

# Define a concrete class for the IPAPI requests strategy
class IPAPIRequestsStrategy(RequestsStrategy):

    # Initialize the IPAPI requests strategy with the IPAPI URL
    def __init__(self):
        super().__init__("http://ip-api.com/line/")

    # Override the get_ip_address method
    def get_ip_address(self):
        # Call the parent method to send the request and get the response
        response = super().get_ip_address()
        # Check if the response is not None
        if response is not None:
            # Parse the response to get the IP address from the last line
            ip_address = response.strip().splitlines()[-1]
            # Return the IP address
            return ip_address
        else:
            # Return None if the response is None
            return None

# Define a class for the IP finder context
class IPFinder:

    # Initialize the IP finder with a strategy
    def __init__(self, strategy:IPFinderStrategy):
        self.strategy = strategy

    # Set a new strategy
    def set_strategy(self, strategy):
        self.strategy = strategy

    # Get the IP address using the current strategy
    def get_ip_address(self):
        return self.strategy.get_ip_address()





if __name__ == "__main__":
    def self_test():
        # Create an IP finder object with the socket strategy
        ip_finder = IPFinder(IPIFYRequestsStrategy())

        # Get the IP address using the socket strategy
        ip_address = ip_finder.get_ip_address()
        print(f"My IP address using the IPIFYRequestsStrategy strategy is {ip_address}")

        # Set the requests strategy
        ip_finder.set_strategy(IPAPIRequestsStrategy())

        # Get the IP address using the requests strategy
        ip_address = ip_finder.get_ip_address()
        print(f"My IP address using the IPAPIRequestsStrategy strategy is {ip_address}")
    
    self_test()