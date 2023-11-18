# Import the requests module
import requests

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