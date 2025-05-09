"""
NBA API Endpoint Analyzer

Core functionality for analyzing NBA API endpoints.
"""

import json
import time
import re
from datetime import datetime

from nba_api.stats.library.http import NBAStatsHTTP
from nba_api.stats.library.parameters import *

from .response_parser import ResponseParser
from .parameter_store import ParameterStore


class EndpointAnalyzer:
    """Analyzer for NBA API endpoints."""

    def __init__(self, endpoint_class_or_name, parameter_store=None):
        """
        Initialize the analyzer with an endpoint class or name.

        Args:
            endpoint_class_or_name: Either a class object or string name of an endpoint
            parameter_store: Optional ParameterStore instance for retrieving known parameters
        """
        # Initialize with the endpoint class or name
        self.endpoint_class = self._resolve_endpoint(endpoint_class_or_name)
        self.endpoint_name = self.endpoint_class.__name__

        # Initialize the parameter store
        self.parameter_store = parameter_store or ParameterStore()

        # Configure testing parameters
        self.retry_attempts = 3
        self.pause_time = 0.6  # Seconds between API calls
        self.timeout = 30  # Seconds

        # Initialize response parser
        self.parser = ResponseParser()

        # Common regex patterns
        self.missing_parameter_regex = r"^\s*?(?:The value '[^']+' is not valid for |The )?([A-z0-9]+( Scope| Category)?)(?: Year)?\\s*(?:property (?:is|are) required\\.?| (?:is|are) required\\.?(?:,? pass 0 for (?:default|all teams))?|\\.)$"
        self.parameter_pattern_regex = r"\\s*The field ([A-z]+) must match the regular expression '([^']+)'\\.(,|;|$)"

        # Store analysis results
        self.result = {
            "status": "pending",
            "endpoint": self.endpoint_name,
            "parameters": [],
            "required_parameters": [],
            "nullable_parameters": [],
            "parameter_patterns": {},
            "data_sets": {},
            "last_validated_date": str(datetime.now().date()),
        }

    def _resolve_endpoint(self, endpoint_class_or_name):
        """
        Resolve the endpoint class from a class object or name.

        Args:
            endpoint_class_or_name: Either a class object or string name

        Returns:
            The endpoint class object

        Raises:
            ValueError: If the endpoint cannot be found
        """
        if isinstance(endpoint_class_or_name, str):
            # Try to import from nba_api.stats.endpoints
            try:
                # Import the package (not with *)
                import nba_api.stats.endpoints as endpoints

                # Try to get the class by name
                if hasattr(endpoints, endpoint_class_or_name):
                    return getattr(endpoints, endpoint_class_or_name)

                # If not found, try to import the specific module
                module_name = endpoint_class_or_name.lower()
                try:
                    module = __import__(
                        f"nba_api.stats.endpoints.{module_name}",
                        fromlist=[endpoint_class_or_name],
                    )
                    if hasattr(module, endpoint_class_or_name):
                        return getattr(module, endpoint_class_or_name)
                except (ImportError, AttributeError):
                    pass

                raise ValueError(f"Endpoint {endpoint_class_or_name} not found")
            except ImportError as e:
                raise ValueError(f"Error importing endpoints: {e}")
        else:
            # Assume it's already a class
            return endpoint_class_or_name

    def set_retry_attempts(self, attempts):
        """Set the number of retry attempts for API calls."""
        self.retry_attempts = attempts
        return self

    def set_pause_time(self, seconds):
        """Set the pause time between API calls."""
        self.pause_time = seconds
        return self

    def set_timeout(self, seconds):
        """Set the timeout for API calls."""
        self.timeout = seconds
        return self

    def analyze(self):
        """
        Analyze the endpoint by running a series of tests.

        Returns:
            dict: Analysis results including parameters, data_sets, etc.
        """
        # Reset the results
        self.result = {
            "status": "pending",
            "endpoint": self.endpoint_name,
            "parameters": [],
            "required_parameters": [],
            "nullable_parameters": [],
            "parameter_patterns": {},
            "data_sets": {},
            "last_validated_date": str(datetime.now().date()),
        }

        # Step 1: Test for required parameters
        self._test_required_parameters()

        # If the endpoint is deprecated, we can stop here
        if self.result["status"] == "deprecated":
            return self.result

        # Step 2: Test with minimal required parameters
        self._test_minimal_requirements()

        # Step 3: Test for nullable parameters
        self._test_nullable_parameters()

        # Step 4: Test with invalid values to get parameter patterns
        self._test_invalid_values()

        # Step 5: Clean up the parameters
        self._clean_parameters()

        # Step 6: Sort the parameters alphabetically
        self.result["parameters"].sort()
        self.result["required_parameters"].sort()
        self.result["nullable_parameters"].sort()

        return self.result

    def _test_required_parameters(self):
        """Test the endpoint with no parameters to identify required parameters."""
        response = self._make_api_request({})

        # Check if the endpoint is deprecated
        if (
            "<title>NBA.com/Stats  | 404 Page Not Found </title>"
            in response.get_response()
        ):
            self.result["status"] = "deprecated"
            return

        # Get required parameters from the response
        required_parameters = self.parser.extract_required_parameters(
            response, self.endpoint_name
        )

        # Add required parameters to the result
        self.result["required_parameters"] = required_parameters

        # Set status to success by default
        self.result["status"] = "success"

    def _test_minimal_requirements(self):
        """Test the endpoint with minimal required parameters."""
        # Prepare the minimal parameters
        required_params = {}

        # Get parameter values from our store or from defaults
        for param in self.result["required_parameters"]:
            # Try to get from parameter store first
            stored_params = self.parameter_store.get_required_parameters(
                self.endpoint_name
            )
            if param in stored_params:
                required_params[param] = stored_params[param]
                continue

            # Otherwise, use default values from parameters library
            # This would be better handled through dependency injection
            if param in parameter_map:
                if len(parameter_map[param]["non-nullable"]):
                    map_key = "non-nullable"
                else:
                    map_key = "nullable"
                parameter_info_key = list(parameter_map[param][map_key].values())[0]
                parameter_info = parameter_variations[parameter_info_key]
                required_params[param] = parameter_info["parameter_value"]
            else:
                print(f'Property "{param}" not in parameter_map')
                self.result["status"] = "invalid"
                required_params[param] = "0"

        # Make the API request with the minimal parameters
        response = self._make_api_request(required_params)

        # Test if we got a valid response
        if response.valid_json():
            # Extract data sets from the response
            data_sets = response.get_headers_from_data_sets()
            self.result["data_sets"] = data_sets

            # Update the parameters list
            all_parameters = list(required_params.keys())
            response_parameters = response.get_parameters()
            if response_parameters:
                all_parameters.extend(list(response_parameters.keys()))
            self.result["parameters"] = list(set(all_parameters))
        else:
            self.result["status"] = "invalid"
            print(f"{self.endpoint_name}: Failed to pass minimal values test")

    def _test_nullable_parameters(self):
        """Test which parameters can be null/empty."""
        # Skip certain endpoints that we know don't support nullable parameters
        skip_endpoints = [
            "BoxScoreAdvancedV2",
            "BoxScoreFourFactorsV2",
            "BoxScoreMiscV2",
            "BoxScoreScoringV2",
            "BoxScoreTraditionalV2",
            "BoxScoreUsageV2",
            "WinProbabilityPBP",
            "AllTimeLeadersGrids",
            "GLAlumBoxScoreSimilarityScore",
            "PlayerEstimatedMetrics",
            "TeamEstimatedMetrics",
        ]

        if self.endpoint_name.lower() in [ep.lower() for ep in skip_endpoints]:
            return

        # Create parameters with empty values
        params = {
            param: ""
            for param in self.result["parameters"]
            if param not in ["DefenseCategory"]  # Always non-nullable
        }

        # Make the API request with empty parameters
        response = self._make_api_request(params)

        # Check for errors in the response
        if (
            "An error has occurred." in response.get_response()
            or "A value is required" in response.get_response()
        ):
            print(f"{self.endpoint_name}: Nullable parameters test failed")
            return

        # Get the required parameters from the response
        required_parameters = self.parser.extract_required_parameters(
            response, self.endpoint_name
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

        # Update the nullable parameters in the result
        self.result["nullable_parameters"].extend(nullable_parameters)
        self.result["nullable_parameters"] = list(
            set(self.result["nullable_parameters"])
        )

    def _test_invalid_values(self):
        """Test with invalid parameter values to identify parameter patterns."""
        # Create parameters with invalid values
        all_params_errors = {}

        for param in self.result["parameters"]:
            # Try to get from parameter store first
            stored_params = self.parameter_store.get_required_parameters(
                self.endpoint_name
            )

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

        # Make the API request with invalid parameters
        response = self._make_api_request(all_params_errors)

        # Get the parameter patterns from the response
        parameter_patterns = self.parser.extract_parameter_patterns(response)

        # Update the parameter patterns in the result
        self.result["parameter_patterns"] = parameter_patterns

        # Verify that we got patterns for all parameters
        if len(parameter_patterns) != len(self.result["parameters"]):
            print(
                f"{self.endpoint_name}: Length of patterns does not equal all parameters",
                parameter_patterns,
                self.result["parameters"],
            )
            self.result["status"] = "invalid"

    def _clean_parameters(self):
        """Clean up the parameters."""
        # Handle parameter overrides
        # This would come from configuration or the parameter store
        parameter_overrides = self.parameter_store.get_parameter_overrides(
            self.endpoint_name
        )

        if parameter_overrides:
            for old_param, new_param in parameter_overrides.items():
                # Update parameters
                if old_param in self.result["parameters"]:
                    self.result["parameters"].remove(old_param)
                    self.result["parameters"].append(new_param)

                # Update required parameters
                if old_param in self.result["required_parameters"]:
                    self.result["required_parameters"].remove(old_param)
                    self.result["required_parameters"].append(new_param)

                # Update nullable parameters
                if old_param in self.result["nullable_parameters"]:
                    self.result["nullable_parameters"].remove(old_param)
                    self.result["nullable_parameters"].append(new_param)

                # Update parameter patterns
                if old_param in self.result["parameter_patterns"]:
                    self.result["parameter_patterns"][new_param] = self.result[
                        "parameter_patterns"
                    ][old_param]
                    del self.result["parameter_patterns"][old_param]

        # Remove any parameters that should not be nullable
        remove_nullable = self.parameter_store.get_remove_nullable_parameters(
            self.endpoint_name
        )

        if remove_nullable:
            for param in remove_nullable:
                if param in self.result["nullable_parameters"]:
                    self.result["nullable_parameters"].remove(param)

    def _make_api_request(self, parameters):
        """Make an API request with the specified parameters."""
        attempt = 0
        while attempt < self.retry_attempts:
            attempt += 1
            try:
                response = NBAStatsHTTP().send_api_request(
                    endpoint=self.endpoint_name,
                    parameters=parameters,
                    timeout=self.timeout,
                )
                return response
            except Exception as e:
                print(f"Error in API request: {e}")
                time.sleep(self.pause_time)

        # If we get here, all attempts failed
        raise Exception(f"Failed to get response after {self.retry_attempts} attempts")


def analyze_endpoint(endpoint_name_or_class, retry_attempts=3, pause_time=0.6):
    """
    Convenience function to analyze a single endpoint.

    Args:
        endpoint_name_or_class: Name or class of the endpoint to analyze
        retry_attempts: Number of retry attempts for API calls
        pause_time: Pause time between API calls in seconds

    Returns:
        dict: Analysis results
    """
    analyzer = EndpointAnalyzer(endpoint_name_or_class)
    analyzer.set_retry_attempts(retry_attempts)
    analyzer.set_pause_time(pause_time)
    return analyzer.analyze()


if __name__ == "__main__":
    # Test the analyzer with a simple endpoint
    result = analyze_endpoint("CommonPlayerInfo")
    print(json.dumps(result, indent=2))
