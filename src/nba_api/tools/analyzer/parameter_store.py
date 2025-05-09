"""
NBA API Parameter Store

Stores and retrieves parameter configurations for NBA API endpoints.
"""

import os
import json
import inspect


class ParameterStore:
    """Store for NBA API parameters."""
    
    def __init__(self, file_path=None):
        """
        Initialize the parameter store.
        
        Args:
            file_path: Optional path to a parameter file
        """
        if file_path is None:
            # Default to a file in the package directory
            package_dir = os.path.dirname(os.path.abspath(__file__))
            file_path = os.path.join(package_dir, 'endpoint_parameters.json')
            
        self.file_path = file_path
        self.parameters = self._load()
        
        # Fallback configurations for endpoints
        self._init_fallback_configs()
        
    def _load(self):
        """Load parameters from the file."""
        if os.path.exists(self.file_path):
            try:
                with open(self.file_path, 'r') as f:
                    return json.load(f)
            except json.JSONDecodeError:
                print(f"Warning: Invalid JSON in {self.file_path}")
        
        return {}
        
    def save(self):
        """Save parameters to the file."""
        with open(self.file_path, 'w') as f:
            json.dump(self.parameters, f, indent=2)
    
    def get_required_parameters(self, endpoint_name):
        """
        Get required parameters for an endpoint.
        
        Args:
            endpoint_name: The name of the endpoint
            
        Returns:
            dict: A dictionary of required parameters and their values
        """
        # Check if we have this endpoint in our parameters
        if endpoint_name in self.parameters:
            return self.parameters[endpoint_name].get("required_parameters", {})
            
        # Fall back to hardcoded configurations
        if endpoint_name in self.missing_required_parameters:
            return self.missing_required_parameters[endpoint_name]
            
        return {}
    
    def get_nullable_parameters(self, endpoint_name):
        """
        Get nullable parameters for an endpoint.
        
        Args:
            endpoint_name: The name of the endpoint
            
        Returns:
            list: A list of nullable parameter names
        """
        # Check if we have this endpoint in our parameters
        if endpoint_name in self.parameters:
            return self.parameters[endpoint_name].get("nullable_parameters", [])
        
        return []
    
    def get_parameter_patterns(self, endpoint_name):
        """
        Get parameter patterns for an endpoint.
        
        Args:
            endpoint_name: The name of the endpoint
            
        Returns:
            dict: A dictionary mapping parameters to their patterns
        """
        # Check if we have this endpoint in our parameters
        if endpoint_name in self.parameters:
            return self.parameters[endpoint_name].get("parameter_patterns", {})
        
        return {}
    
    def get_parameter_overrides(self, endpoint_name):
        """
        Get parameter overrides for an endpoint.
        
        Args:
            endpoint_name: The name of the endpoint
            
        Returns:
            dict: A dictionary mapping old parameter names to new ones
        """
        if endpoint_name in self.parameter_override:
            return self.parameter_override[endpoint_name]
        
        return {}
    
    def get_remove_nullable_parameters(self, endpoint_name):
        """
        Get parameters that should not be nullable for an endpoint.
        
        Args:
            endpoint_name: The name of the endpoint
            
        Returns:
            list: A list of parameter names that should not be nullable
        """
        if endpoint_name in self.remove_nullable_parameters:
            return self.remove_nullable_parameters[endpoint_name]
        
        return []
    
    def update_from_analysis(self, endpoint_name, analysis_result):
        """
        Update the store with analysis results.
        
        Args:
            endpoint_name: The name of the endpoint
            analysis_result: The analysis result dictionary
        """
        if endpoint_name not in self.parameters:
            self.parameters[endpoint_name] = {}
            
        # Convert required parameters from list to dict
        required_params = {}
        for param in analysis_result.get("required_parameters", []):
            if param in self.parameters.get(endpoint_name, {}).get("required_parameters", {}):
                # Keep existing value
                required_params[param] = self.parameters[endpoint_name]["required_parameters"][param]
            elif endpoint_name in self.missing_required_parameters and param in self.missing_required_parameters[endpoint_name]:
                # Use value from fallback
                required_params[param] = self.missing_required_parameters[endpoint_name][param]
            else:
                # Default to empty string
                required_params[param] = ""
        
        self.parameters[endpoint_name]["required_parameters"] = required_params
        self.parameters[endpoint_name]["nullable_parameters"] = analysis_result.get("nullable_parameters", [])
        self.parameters[endpoint_name]["parameter_patterns"] = analysis_result.get("parameter_patterns", {})
        self.parameters[endpoint_name]["last_validated_date"] = analysis_result.get("last_validated_date", "")
        
        self.save()
    
    def _init_fallback_configs(self):
        """Initialize fallback configurations."""
        # Import parameter data from NBA API
        # This is temporary and should be moved to a proper configuration
        from nba_api.stats.library.parameters import *
        
        # Missing required parameters by endpoint
        self.missing_required_parameters = {
            "AllTimeLeadersGrids": {
                "TopX": "10",
                "LeagueID": LeagueID.default,
                "PerMode": PerModeSimple.default,
                "SeasonType": SeasonType.default,
            },
            "CumeStatsTeamGames": {"Season": Season.default},
            "DefenseHub": {"Season": "2017-18"},
            "DraftBoard": {"Season": SeasonYear.default},
            "GLAlumBoxScoreSimilarityScore": {
                "Person1Id": "2544",
                "Person2Id": "2544",
                "Person1LeagueId": LeagueID.default,
                "Person1Season": SeasonYear.default,
                "Person1SeasonType": SeasonType.default,
                "Person2LeagueId": LeagueID.default,
                "Person2Season": SeasonYear.default,
                "Person2SeasonType": SeasonType.default,
            },
            "LeagueDashLineups": {"Season": Season.default},
            "LeagueDashPlayerClutch": {"Season": Season.default},
            "LeagueDashPlayerStats": {"Season": Season.default},
            "LeagueDashTeamClutch": {"Season": Season.default},
            "LeagueDashTeamShotLocations": {"Season": Season.default},
            "LeagueDashTeamStats": {"Season": Season.default},
            "LeagueGameLog": {"Counter": 0, "Season": Season.default},
            "LeagueHustleStatsPlayer": {"Season": Season.default},
            "LeagueHustleStatsTeam": {"Season": Season.default},
            "LeagueLeaders": {"Season": Season.default},
            "LeagueLineupViz": {"Season": Season.default},
            "LeaguePlayerOnDetails": {
                "Season": Season.default,
                "TeamID": "1610612739",
            },  # Cleveland Cavaliers
            "LeagueStandings": {"Season": Season.default},
            "LeagueStandingsV3": {"Season": Season.default},
            "PlayerCareerByCollege": {"College": "Ohio State"},
            "PlayerCompare": {"Season": Season.default},
            "PlayerDashboardByClutch": {"Season": Season.default},
            "PlayerDashboardByGameSplits": {"Season": Season.default},
            "PlayerDashboardByGeneralSplits": {"Season": Season.default},
            "PlayerDashboardByLastNGames": {"Season": Season.default},
            "PlayerDashboardByShootingSplits": {"Season": Season.default},
            "PlayerDashboardByTeamPerformance": {"Season": Season.default},
            "PlayerDashboardByYearOverYear": {"Season": Season.default},
            "PlayerDashPtPass": {"LeagueID": LeagueID.default},
            "PlayerDashPtReb": {"LeagueID": LeagueID.default},
            "PlayerDashPtShotDefend": {"LeagueID": LeagueID.default},
            "PlayerDashPtShots": {"LeagueID": LeagueID.default},
            "PlayerEstimatedMetrics": {
                "LeagueID": LeagueID.default,
                "Season": Season.default,
                "SeasonType": SeasonType.default,
            },
            "PlayerFantasyProfile": {"Season": Season.default},
            "PlayerFantasyProfileBarGraph": {"Season": Season.default},
            "PlayerVsPlayer": {"Season": Season.default},
            "ShotChartDetail": {
                "ContextMeasure": ContextMeasureSimple.default,
                "LeagueID": LeagueID.default,
                "PlayerPosition": "",
            },
            "ShotChartLeagueWide": {"LeagueID": LeagueID.default},
            "ShotChartLineupDetail": {"GameID": "", "TeamID": ""},
            "TeamAndPlayersVsPlayers": {"Season": Season.default},
            "TeamDashboardByGeneralSplits": {"Season": Season.default},
            "TeamDashboardByShootingSplits": {"Season": Season.default},
            "TeamDashLineups": {"Season": Season.default},
            "TeamDashPtPass": {"LeagueID": LeagueID.default},
            "TeamDashPtReb": {"LeagueID": LeagueID.default},
            "TeamDashPtShots": {"LeagueID": LeagueID.default},
            "TeamEstimatedMetrics": {
                "LeagueID": LeagueID.default,
                "Season": Season.default,
                "SeasonType": SeasonType.default,
            },
            "TeamPlayerDashboard": {"Season": Season.default},
            "TeamPlayerOnOffDetails": {"Season": Season.default},
            "TeamPlayerOnOffSummary": {"Season": Season.default},
            "TeamVsPlayer": {
                "Season": Season.default,
                "TeamID": "1610612739",
            },  # Cleveland Cavaliers
            "VideoDetails": {"Season": Season.default},
        }
        
        # Parameter overrides
        self.parameter_override = {
            "PlayerCareerByCollege": {"School": "College"},
            "PlayerGameLogs": {"SeasonYear": "Season"},
            "TeamGameLogs": {"SeasonYear": "Season"},
        }
        
        # Parameters that should not be nullable
        self.remove_nullable_parameters = {"PlayerCareerByCollege": ["School"]}


if __name__ == "__main__":
    # Test the parameter store
    store = ParameterStore()
    print(f"Number of endpoints with fallback configs: {len(store.missing_required_parameters)}")
    
    # Test getting parameters for a specific endpoint
    endpoint = "PlayerCareerByCollege"
    required_params = store.get_required_parameters(endpoint)
    print(f"Required parameters for {endpoint}: {required_params}")
    
    # Test parameter overrides
    overrides = store.get_parameter_overrides(endpoint)
    print(f"Parameter overrides for {endpoint}: {overrides}")
