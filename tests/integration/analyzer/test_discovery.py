"""
Tests for NBA API Endpoint Discovery

Tests for discovering endpoints from the nba_api package.
"""

import pytest
from nba_api.tools.analyzer import discover_endpoints, discover_endpoints_from_files


class TestDiscovery:
    """Tests for endpoint discovery functions."""
    
    def test_discover_endpoints(self):
        """Test the discover_endpoints function."""
        endpoints = discover_endpoints()
        
        # We should find at least a few endpoints
        assert len(endpoints) > 0
        
        # Check for some common endpoint classes
        common_endpoints = [
            'CommonPlayerInfo',
            'LeagueLeaders',
            'BoxScoreSummaryV2',
        ]
        
        for endpoint in common_endpoints:
            assert endpoint in endpoints, f"Expected to find {endpoint} endpoint"
    
    def test_discover_endpoints_from_files(self):
        """Test the discover_endpoints_from_files function."""
        endpoints = discover_endpoints_from_files()
        
        # We should find at least a few endpoints
        assert len(endpoints) > 0
        
        # Check for some common endpoint classes
        common_endpoints = [
            'CommonPlayerInfo',
            'LeagueLeaders',
            'BoxScoreSummaryV2',
        ]
        
        for endpoint in common_endpoints:
            assert endpoint in endpoints, f"Expected to find {endpoint} endpoint"
    
    def test_endpoints_have_required_attributes(self):
        """Test that discovered endpoints have the required attributes."""
        endpoints = discover_endpoints()
        
        # Check a sample endpoint
        endpoint_name = 'CommonPlayerInfo'
        if endpoint_name in endpoints:
            endpoint_class = endpoints[endpoint_name]
            
            # Check that it has the necessary attributes
            assert hasattr(endpoint_class, '__module__')
            assert 'nba_api.stats.endpoints' in endpoint_class.__module__
