"""
Required Parameters Test Command

Tests an endpoint with no parameters to identify which parameters are required.
"""

from nba_api.stats.library.http import NBAStatsHTTP
import re


class RequiredParametersCommand:
    """Command for testing required parameters."""
    
    def __init__(self, parser):
        """
        Initialize the command.
        
        Args:
            parser: ResponseParser instance for parsing responses
        """
        self.parser = parser
        
    def execute(self, endpoint_name):
        """
        Execute the command.
        
        Args:
            endpoint_name: Name of the endpoint to test
            
        Returns:
            tuple: (status, required_parameters)
        """
        # Send a request with no parameters
        response = NBAStatsHTTP().send_api_request(
            endpoint=endpoint_name, 
            parameters={}
        )
        
        # Check if the endpoint is deprecated
        if "<title>NBA.com/Stats  | 404 Page Not Found </title>" in response.get_response():
            return "deprecated", []
            
        # Get required parameters from the response
        required_parameters = self.parser.extract_required_parameters(response, endpoint_name)
        
        return "success", required_parameters
