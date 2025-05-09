"""
Tests for NBA API Parameter Store

Tests for storing and retrieving parameter configurations.
"""

import os
import json
import tempfile
import pytest
from nba_api.tools.analyzer import ParameterStore


class TestParameterStore:
    """Tests for the ParameterStore class."""
    
    @pytest.fixture
    def temp_param_file(self):
        """Create a temporary parameter file for testing."""
        # Create a temporary file
        with tempfile.NamedTemporaryFile(delete=False, suffix='.json') as f:
            # Write some test data
            test_data = {
                "CommonPlayerInfo": {
                    "required_parameters": {
                        "PlayerID": "2544"
                    },
                    "nullable_parameters": ["Season", "LeagueID"],
                    "parameter_patterns": {
                        "PlayerID": "^\\d+$"
                    },
                    "last_validated_date": "2025-01-01"
                }
            }
            f.write(json.dumps(test_data).encode('utf-8'))
            
        # Return the file path
        file_path = f.name
        yield file_path
        
        # Clean up
        try:
            os.unlink(file_path)
        except (OSError, IOError) as e:
            # Log the error but continue with the test
            print(f"Failed to clean up temporary file: {e}")
    
    def test_load_from_file(self, temp_param_file):
        """Test loading parameters from a file."""
        store = ParameterStore(file_path=temp_param_file)
        
        # Check that the parameters were loaded
        assert "CommonPlayerInfo" in store.parameters
        assert "required_parameters" in store.parameters["CommonPlayerInfo"]
        assert "PlayerID" in store.parameters["CommonPlayerInfo"]["required_parameters"]
        assert store.parameters["CommonPlayerInfo"]["required_parameters"]["PlayerID"] == "2544"
    
    def test_get_required_parameters(self, temp_param_file):
        """Test getting required parameters for an endpoint."""
        store = ParameterStore(file_path=temp_param_file)
        
        # Get required parameters for an endpoint
        required_params = store.get_required_parameters("CommonPlayerInfo")
        
        # Check that the correct parameters were returned
        assert "PlayerID" in required_params
        assert required_params["PlayerID"] == "2544"
    
    def test_get_nullable_parameters(self, temp_param_file):
        """Test getting nullable parameters for an endpoint."""
        store = ParameterStore(file_path=temp_param_file)
        
        # Get nullable parameters for an endpoint
        nullable_params = store.get_nullable_parameters("CommonPlayerInfo")
        
        # Check that the correct parameters were returned
        assert "Season" in nullable_params
        assert "LeagueID" in nullable_params
    
    def test_save_and_load(self):
        """Test saving and loading parameters."""
        # Create a temporary file
        with tempfile.NamedTemporaryFile(delete=False, suffix='.json') as f:
            file_path = f.name
            
        try:
            # Create a store and add some parameters
            store = ParameterStore(file_path=file_path)
            store.parameters["TestEndpoint"] = {
                "required_parameters": {
                    "TestParam": "test_value"
                },
                "nullable_parameters": ["NullableParam"],
                "parameter_patterns": {
                    "TestParam": "^test_.*$"
                },
                "last_validated_date": "2025-01-01"
            }
            
            # Save the parameters
            store.save()
            
            # Create a new store that loads from the file
            new_store = ParameterStore(file_path=file_path)
            
            # Check that the parameters were loaded
            assert "TestEndpoint" in new_store.parameters
            assert "required_parameters" in new_store.parameters["TestEndpoint"]
            assert "TestParam" in new_store.parameters["TestEndpoint"]["required_parameters"]
            assert new_store.parameters["TestEndpoint"]["required_parameters"]["TestParam"] == "test_value"
        finally:
            # Clean up
            try:
                os.unlink(file_path)
            except (OSError, IOError) as e:
                # Log the error but continue with the test
                print(f"Failed to clean up temporary file: {e}")
    
    def test_update_from_analysis(self):
        """Test updating parameters from analysis results."""
        # Create a temporary file
        with tempfile.NamedTemporaryFile(delete=False, suffix='.json') as f:
            file_path = f.name
            
        try:
            # Create a store
            store = ParameterStore(file_path=file_path)
            
            # Create a test analysis result
            analysis_result = {
                "status": "success",
                "endpoint": "TestEndpoint",
                "parameters": ["Param1", "Param2"],
                "required_parameters": ["Param1"],
                "nullable_parameters": ["Param2"],
                "parameter_patterns": {
                    "Param1": "^\\d+$",
                    "Param2": "^\\w+$"
                },
                "data_sets": {},
                "last_validated_date": "2025-01-01"
            }
            
            # Update from the analysis result
            store.update_from_analysis("TestEndpoint", analysis_result)
            
            # Check that the parameters were updated
            assert "TestEndpoint" in store.parameters
            assert "required_parameters" in store.parameters["TestEndpoint"]
            assert "Param1" in store.parameters["TestEndpoint"]["required_parameters"]
            assert "nullable_parameters" in store.parameters["TestEndpoint"]
            assert "Param2" in store.parameters["TestEndpoint"]["nullable_parameters"]
        finally:
            # Clean up
            try:
                os.unlink(file_path)
            except (OSError, IOError) as e:
                # Log the error but continue with the test
                print(f"Failed to clean up temporary file: {e}")
