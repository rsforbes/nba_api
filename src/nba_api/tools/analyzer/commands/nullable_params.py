"""
Nullable Parameters Test Command

Tests which parameters can be null/empty by sending empty values.
"""

from nba_api.stats.library.http import NBAStatsHTTP


class NullableParametersCommand:
    """Command for testing nullable parameters."""

    def __init__(self, parser):
        """
        Initialize the command.

        Args:
            parser: ResponseParser instance for parsing responses
        """
        self.parser = parser

        # List of known non-nullable parameters
        self.non_nullable_list = ["DefenseCategory"]

        # Skip these endpoints because they don't support nullable parameters
        self.skip_endpoints = [
            "boxscoreadvancedv2",
            "boxscorefourfactorsv2",
            "boxscoremiscv2",
            "boxscorescoringv2",
            "boxscoretraditionalv2",
            "boxscoreusagev2",
            "winprobabilitypbp",
            "alltimeleadersgrids",
            "glalumboxscoresimilarityscore",
            "playerestimatedmetrics",
            "teamestimatedmetrics",
        ]

    def execute(self, endpoint_name, all_parameters):
        """
        Execute the command.

        Args:
            endpoint_name: Name of the endpoint to test
            all_parameters: List of all parameters for the endpoint

        Returns:
            list: List of nullable parameters
        """
        # Skip endpoints that don't support nullable parameters
        if endpoint_name.lower() in self.skip_endpoints:
            return []

        # Create parameters with empty values
        params = {
            param: "" for param in all_parameters if param not in self.non_nullable_list
        }

        # Send a request with empty parameters
        response = NBAStatsHTTP().send_api_request(
            endpoint=endpoint_name, parameters=params
        )

        # Check for errors in the response
        if (
            "An error has occurred." in response.get_response()
            or "A value is required" in response.get_response()
        ):
            print(f"{endpoint_name}: Nullable parameters test failed")
            return []

        # Get the required parameters from the response
        required_parameters = self.parser.extract_required_parameters(
            response, endpoint_name
        )

        # Parameters that are not required are nullable
        nullable_parameters = [
            param for param in list(params.keys()) if param not in required_parameters
        ]

        # Also check the response parameters
        if response.get_parameters():
            response_parameters = response.get_parameters()
            for parameter, value in response_parameters.items():
                if value is None or value == "":
                    nullable_parameters.append(parameter)

        return list(set(nullable_parameters))
