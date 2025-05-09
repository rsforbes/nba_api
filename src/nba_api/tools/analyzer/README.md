# NBA API Endpoint Analyzer

A toolkit for analyzing, testing, and validating NBA.com API endpoints.

## Features

- Discover available endpoints in the nba_api package
- Test endpoints for required and nullable parameters
- Identify parameter validation patterns
- Store and retrieve parameter configurations
- Command-line interface for easy testing

## Usage

### From Python

```python
from nba_api.tools.analyzer import analyze_endpoint, discover_endpoints

# Analyze a specific endpoint
result = analyze_endpoint("CommonPlayerInfo")
print(result["required_parameters"])  # ['PlayerID']

# Get all available endpoints
endpoints = discover_endpoints()
print(f"Found {len(endpoints)} endpoints")
```

### From Command Line

```bash
# List all available endpoints
nba-analyze --list

# Analyze a specific endpoint
nba-analyze --endpoint CommonPlayerInfo

# Analyze all endpoints and save results to a file
nba-analyze --all --output analysis.json
```

## Development

Run the tests:

```bash
pytest tests/integration/analyzer/
```
