"""
Backward Compatibility Module for Endpoint Analysis

This module provides backward compatibility with the old endpoint analysis API.
It imports and redirects to the new nba_api.tools.analyzer package.
"""

import warnings
from nba_api.tools.analyzer import EndpointAnalyzer, discover_endpoints

warnings.warn(
    "This module is deprecated. Please use nba_api.tools.analyzer instead.",
    DeprecationWarning,
    stacklevel=2
)


def analyze_endpoint(endpoint):
    """Legacy function for analyzing a specific endpoint."""
    analyzer = EndpointAnalyzer(endpoint)
    return analyzer.analyze()


def analyze_and_save_all_endpoints(*args, **kwargs):
    """Legacy function for analyzing all endpoints."""
    # Import the function from the new location
    from nba_api.tools.analyzer.cli import analyze_all_endpoints
    return analyze_all_endpoints(*args, **kwargs)


def analyze_endpoint_with_attempts(endpoint, attempts=5, pause=1):
    """Legacy function for analyzing an endpoint with retry attempts."""
    from nba_api.tools.analyzer.cli import analyze_endpoint_with_retry
    return analyze_endpoint_with_retry(endpoint, retry_attempts=attempts, pause=pause)


def analyze_all_endpoints_with_threading():
    """Legacy function for analyzing all endpoints with threading."""
    from nba_api.tools.analyzer.cli import analyze_all_endpoints
    return analyze_all_endpoints()
