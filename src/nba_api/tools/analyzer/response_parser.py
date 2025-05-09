"""
NBA API Response Parser

Parses NBA API responses to extract parameter information.
"""

import re


class ResponseParser:
    """Parser for NBA API responses."""

    def __init__(self):
        """Initialize the response parser."""
        # Regular expressions for parsing responses
        self.missing_parameter_regex = r"^\\s*?(?:The value '[^']+' is not valid for |The )?([A-z0-9]+( Scope| Category)?)(?: Year)?\\s*(?:property (?:is|are) required\\.?| (?:is|are) required\\.?(?:,? pass 0 for (?:default|all teams))?|\\.)$"
        self.parameter_pattern_regex = r"\\s*The field ([A-z]+) must match the regular expression '([^']+)'\\.(;|$)"

    def extract_parameter_patterns(self, nba_stats_response):
        """
        Extract parameter patterns from an error response.

        Args:
            nba_stats_response: The NBAStatsHTTP response object

        Returns:
            dict: A dictionary mapping parameters to their patterns
        """
        parameter_patterns = {}

        # Check if it's an HTML response
        if re.search("<.*?>", nba_stats_response.get_response()):
            # HTML Response, no patterns to extract
            return parameter_patterns

        # Split the response into matches
        matches = nba_stats_response.get_response().split(";")

        for match in matches:
            parameter_regex_match = re.match(self.parameter_pattern_regex, match)
            invalid_parameter_match = re.match(self.missing_parameter_regex, match)

            prop = None
            pattern = None

            if parameter_regex_match:
                prop = parameter_regex_match.group(1)
                pattern = parameter_regex_match.group(2)
                prop = prop.replace(" ", "")
                parameter_patterns[prop] = pattern
            elif invalid_parameter_match:
                prop = invalid_parameter_match.group(1)
                prop = prop.replace(" ", "")
                # No pattern for invalid parameters
            elif match in [
                " Invalid date",
                "<e><Message>An error has occurred.</Message></e>",
                "Invalid game date",
                " Invalid game date",
            ]:
                # Ignored error messages
                pass
            elif nba_stats_response.valid_json():
                # Valid JSON response, no patterns to extract
                pass
            elif (
                not parameter_regex_match
                and not invalid_parameter_match
                and "Invalid date" not in nba_stats_response.get_response()
                and "must be between" not in nba_stats_response.get_response()
            ):
                # Unhandled error message
                print(f"Warning: Failed to match error: {match}")

        return parameter_patterns

    def extract_required_parameters(self, nba_stats_response, endpoint_name):
        """
        Extract required parameters from an error response.

        Args:
            nba_stats_response: The NBAStatsHTTP response object
            endpoint_name: The name of the endpoint

        Returns:
            list: A list of required parameter names
        """
        required_parameters = []

        # Skip if it's a valid JSON response
        if nba_stats_response.valid_json():
            return required_parameters

        # Check if it's an HTML response
        if re.search("<.*?>", nba_stats_response.get_response()):
            # HTML Response, no parameters to extract
            return required_parameters

        # Split the response into matches
        matches = nba_stats_response.get_response().split(";")

        for match in matches:
            required_parameter = re.match(self.missing_parameter_regex, match)

            if not required_parameter:
                # Not a required parameter error message
                continue

            # Extract the parameter name
            param_name = required_parameter.group(1).replace(" ", "")

            # Fix case sensitivity
            if param_name == "Runtype":
                param_name = "RunType"

            required_parameters.append(param_name)

        return required_parameters


if __name__ == "__main__":
    # Test code here
    pass
