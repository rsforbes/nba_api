"""
Invalid Values Test Command

Tests with invalid parameter values to identify parameter patterns.
"""

from nba_api.stats.library.http import NBAStatsHTTP
from nba_api.stats.library.parameters import parameter_map, parameter_variations


class InvalidValuesCommand:
    """Command for testing invalid values."""

    def __init__(self, parser):
        """
        Initialize the command.

        Args:
            parser: ResponseParser instance for parsing responses
        """
        self.parser = parser

    def execute(self, endpoint_name, all_parameters):
        """
        Execute the command.

        Args:
            endpoint_name: Name of the endpoint to test
            all_parameters: List of all parameters for the endpoint

        Returns:
            dict: A dictionary mapping parameters to their patterns
        """
        # Create parameters with invalid values
        all_params_errors = {}

        for param in all_parameters:
            if param in parameter_map:
                if len(parameter_map[param]["non-nullable"]):
                    map_key = "non-nullable"
                else:
                    map_key = "nullable"
                parameter_info_key = list(parameter_map[param][map_key].values())[0]
                parameter_info = parameter_variations[parameter_info_key]
                all_params_errors[param] = parameter_info["parameter_error_value"]
            else:
                print(f"{param} not found in parameter map - invalid test")
                all_params_errors[param] = "a"

        # Send a request with invalid parameters
        response = NBAStatsHTTP().send_api_request(
            endpoint=endpoint_name, parameters=all_params_errors
        )

        # Extract parameter patterns from the response
        parameter_patterns = self.parser.extract_parameter_patterns(response)

        # Add missing parameters with None pattern
        for param in all_parameters:
            if param not in parameter_patterns:
                parameter_patterns[param] = None

        return parameter_patterns
