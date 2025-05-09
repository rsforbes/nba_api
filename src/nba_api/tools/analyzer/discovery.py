"""
NBA API Endpoint Discovery Module

Utility functions for discovering available endpoints in the nba_api package.
"""

import os
import inspect
import importlib
import pkgutil


def discover_endpoints():
    """
    Dynamically discover all endpoint classes in the nba_api.stats.endpoints module.

    Returns:
        dict: A dictionary mapping endpoint names to their corresponding classes.
    """
    # Import endpoints dynamically to avoid circular imports
    try:
        from nba_api.stats.endpoints import *
        from nba_api.stats.library.http import NBAStatsHTTP
    except ImportError:
        return {}

    endpoints = {}

    # Get all classes from the module
    for name, obj in globals().items():
        # Check if it's a class, not the base class, and from the right module
        if (
            inspect.isclass(obj)
            and obj != NBAStatsHTTP
            and hasattr(obj, "__module__")
            and "nba_api.stats.endpoints" in obj.__module__
        ):

            endpoints[name] = obj

    return endpoints


def discover_endpoints_from_files():
    """
    Discover endpoints by scanning the endpoints directory directly.
    This approach is more robust than the global-based approach.

    Returns:
        dict: A dictionary mapping endpoint names to their corresponding classes.
    """
    endpoints = {}

    try:
        # Get the path to the endpoints directory
        import nba_api.stats.endpoints

        endpoints_dir = os.path.dirname(nba_api.stats.endpoints.__file__)

        # Get the base HTTP class for filtering
        from nba_api.stats.library.http import NBAStatsHTTP

        # Load each endpoint module
        for module_finder, name, ispkg in pkgutil.iter_modules([endpoints_dir]):
            if name == "__init__" or name.startswith("_"):
                continue

            # Import the module
            try:
                module = importlib.import_module(f"nba_api.stats.endpoints.{name}")

                # Look for classes in the module
                for class_name, obj in inspect.getmembers(module, inspect.isclass):
                    if (
                        obj.__module__ == f"nba_api.stats.endpoints.{name}"
                        and obj != NBAStatsHTTP
                    ):

                        endpoints[class_name] = obj
            except (ImportError, AttributeError) as e:
                print(f"Warning: Could not import {name}: {e}")
    except ImportError as e:
        print(f"Error discovering endpoints: {e}")

    return endpoints


if __name__ == "__main__":
    # Test the discovery functions
    endpoints = discover_endpoints_from_files()
    print(f"Discovered {len(endpoints)} endpoints:")
    for name in sorted(endpoints.keys()):
        print(f"  - {name}")
