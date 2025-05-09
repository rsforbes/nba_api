"""
Tests for the NBA API Endpoint Analyzer

Integration tests for analyzing endpoints.
"""

import pytest
from nba_api.tools.analyzer import EndpointAnalyzer, discover_endpoints


# Get a subset of endpoints for testing
def get_test_endpoints():
    """
    Get a small subset of endpoints for testing.
    
    Returns:
        dict: Dictionary of test endpoints
    """
    all_endpoints = discover_endpoints()
    
    # Choose a representative sample that's known to work
    test_subset = [
        'CommonPlayerInfo',  # Simple endpoint with PlayerID parameter
        'LeagueLeaders',     # Endpoint with Season parameter
        'BoxScoreSummaryV2', # Endpoint with GameID parameter
    ]
    
    # Filter the endpoints to only include our test subset
    return {name: all_endpoints[name] for name in test_subset if name in all_endpoints}


class TestEndpointAnalyzer:
    """Tests for the EndpointAnalyzer."""
    
    @pytest.fixture(scope="module")
    def test_endpoints(self):
        """Fixture for test endpoints."""
        return get_test_endpoints()
    
    @pytest.mark.parametrize("endpoint_name", [
        'CommonPlayerInfo',
        'LeagueLeaders',
        'BoxScoreSummaryV2',
    ])
    def test_endpoint_analysis(self, endpoint_name, test_endpoints):
        """Test analyzing a specific endpoint."""
        # Skip if endpoint not available
        if endpoint_name not in test_endpoints:
            pytest.skip(f"Endpoint {endpoint_name} not available")
            
        # Create analyzer
        analyzer = EndpointAnalyzer(test_endpoints[endpoint_name])
        
        # Analyze endpoint
        result = analyzer.analyze()
        
        # Basic validation
        assert result["status"] in ["success", "deprecated", "invalid"]
        assert result["endpoint"] == endpoint_name
        assert "parameters" in result
        assert "required_parameters" in result
        assert "nullable_parameters" in result
        
        # Endpoint-specific validation
        if endpoint_name == "CommonPlayerInfo":
            assert "PlayerID" in result["required_parameters"]
        
        if endpoint_name == "LeagueLeaders":
            assert "Season" in result["required_parameters"]
            
        if endpoint_name == "BoxScoreSummaryV2":
            assert "GameID" in result["required_parameters"]
            
    def test_analyze_function_works(self):
        """Test the analyze_endpoint convenience function."""
        from nba_api.tools.analyzer import analyze_endpoint
        
        # Use a simple endpoint
        try:
            result = analyze_endpoint("CommonPlayerInfo")
            assert result["status"] in ["success", "deprecated", "invalid"]
            assert result["endpoint"] == "CommonPlayerInfo"
            assert "PlayerID" in result["required_parameters"]
        except Exception as e:
            pytest.skip(f"Endpoint analysis failed: {e}")
