# NBA API Endpoint Analyzer

The NBA API Endpoint Analyzer is a tool for analyzing, testing, and validating the endpoints in the NBA.com API. It helps diagnose issues with endpoints, discover parameter requirements, and explore available endpoints.

## Features

- Discover available endpoints in the nba_api package
- Test endpoints for required and nullable parameters
- Identify parameter validation patterns
- Store and retrieve parameter configurations
- Command-line interface for easy testing

## Installation

The analyzer is included with the nba_api package, so no additional installation is needed:

```bash
pip install nba_api
```

## Using the Analyzer in Python

### Analyzing an Endpoint

```python
from nba_api.tools.analyzer import analyze_endpoint

# Analyze a specific endpoint
result = analyze_endpoint("CommonPlayerInfo")

# View the results
print(f"Endpoint Status: {result['status']}")
print(f"Required Parameters: {result['required_parameters']}")
print(f"Nullable Parameters: {result['nullable_parameters']}")
```

### Discovering Available Endpoints

```python
from nba_api.tools.analyzer import discover_endpoints

# Get all available endpoints
endpoints = discover_endpoints()
print(f"Found {len(endpoints)} endpoints")

# Filter endpoints by name
player_endpoints = [name for name in endpoints if "Player" in name]
print(f"Found {len(player_endpoints)} player-related endpoints")
```

### Using the Parameter Store

```python
from nba_api.tools.analyzer import ParameterStore

# Create a parameter store
store = ParameterStore()

# Get required parameters for an endpoint
required_params = store.get_required_parameters("CommonPlayerInfo")
print(required_params)  # {'PlayerID': '2544'} (example value for LeBron James)

# Update the parameter store with analysis results
store.update_from_analysis("CommonPlayerInfo", result)
```

## Using the Command-Line Interface

The nba-analyze command provides a user-friendly interface for analyzing endpoints.

### Listing Available Endpoints

```bash
nba-analyze --list
```

This will display a list of all available endpoints in the nba_api package.

### Analyzing a Specific Endpoint

```bash
nba-analyze --endpoint CommonPlayerInfo
```

This will analyze the CommonPlayerInfo endpoint and display the results.

### Analyzing All Endpoints

```bash
nba-analyze --all --output analysis.json
```

This will analyze all endpoints and save the results to a JSON file.

### Additional Options

```bash
nba-analyze --help
```

This will display all available options for the nba-analyze command.

## Troubleshooting Endpoints

If you're experiencing issues with an NBA API endpoint, you can use the analyzer to diagnose the problem:

1. Check if the endpoint is working:
   ```bash
   nba-analyze --endpoint ProblemEndpoint
   ```

2. Verify required parameters:
   ```python
   from nba_api.tools.analyzer import analyze_endpoint
   result = analyze_endpoint("ProblemEndpoint")
   print(result["required_parameters"])
   ```

3. Test with minimal parameters:
   ```python
   from nba_api.stats.endpoints import problemendpoint
   
   # Using required parameters identified by the analyzer
   response = problemendpoint.ProblemEndpoint(
       parameter1="value1",
       parameter2="value2"
   )
   ```

## Advanced Usage

### Creating a Custom Analyzer

```python
from nba_api.tools.analyzer import EndpointAnalyzer

# Create an analyzer with custom settings
analyzer = EndpointAnalyzer("CommonPlayerInfo")
analyzer.set_retry_attempts(5)
analyzer.set_pause_time(1.0)
analyzer.set_timeout(60)

# Run the analysis
result = analyzer.analyze()
```

### Working with API Responses

```python
from nba_api.tools.analyzer import EndpointAnalyzer
from nba_api.stats.library.http import NBAStatsHTTP

# Make an API request
response = NBAStatsHTTP().send_api_request(
    endpoint="CommonPlayerInfo",
    parameters={"PlayerID": "2544"}
)

# Create an analyzer
analyzer = EndpointAnalyzer("CommonPlayerInfo")

# Parse the response
patterns = analyzer.parser.extract_parameter_patterns(response)
required_params = analyzer.parser.extract_required_parameters(response, "CommonPlayerInfo")
```

## Contributing

If you find issues with endpoints or want to improve the analyzer, please consider contributing to the project. See [CONTRIBUTING.md](../CONTRIBUTING.md) for more information.
