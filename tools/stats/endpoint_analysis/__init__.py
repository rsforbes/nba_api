
NBA API Endpoint Analysis

This package has been deprecated in favor of the new nba_api.tools.analyzer package.
It is kept for backward compatibility only.

import warnings

warnings.warn(
    'The tools.stats.endpoint_analysis package is deprecated. '
    'Please use nba_api.tools.analyzer instead.',
    DeprecationWarning,
    stacklevel=2
)

# Import from our compatibility module
from .analysis_compat import (
    analyze_endpoint,
    analyze_and_save_all_endpoints,
    analyze_endpoint_with_attempts,
    analyze_all_endpoints_with_threading,
)

# Make it look like we're importing from the old module
analysis = type('analysis', (), {
    'analyze_endpoint': analyze_endpoint,
    'analyze_and_save_all_endpoints': analyze_and_save_all_endpoints,
    'analyze_endpoint_with_attempts': analyze_endpoint_with_attempts,
    'analyze_all_endpoints_with_threading': analyze_all_endpoints_with_threading,
})()

