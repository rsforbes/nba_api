"""
NBA API Endpoint Analyzer CLI

Command-line interface for analyzing NBA API endpoints.
"""

import os
import sys
import json
import argparse
import time
from datetime import datetime

from .discovery import discover_endpoints_from_files
from .analyzer import EndpointAnalyzer
from .parameter_store import ParameterStore


def analyze_all_endpoints(endpoints=None, pause=1, parameter_store=None, output_file=None):
    """
    Analyze all endpoints and save the results.
    
    Args:
        endpoints: Optional dictionary of endpoints to analyze
        pause: Pause time between API calls in seconds
        parameter_store: Optional ParameterStore instance
        output_file: Optional file path to save results
        
    Returns:
        dict: A dictionary of analysis results by endpoint name
    """
    # Discover endpoints if not provided
    if endpoints is None:
        endpoints = discover_endpoints_from_files()
        
    # Initialize parameter store if not provided
    if parameter_store is None:
        parameter_store = ParameterStore()
        
    # Initialize results
    results = {}
    
    # Analyze each endpoint
    for name, endpoint_class in endpoints.items():
        print(f"Analyzing {name}...")
        try:
            # Check if the endpoint already has valid results
            if name in parameter_store.parameters and parameter_store.parameters[name].get("status") in ["success", "deprecated"]:
                print(f"  Using cached results for {name}")
                results[name] = parameter_store.parameters[name]
                continue
                
            # Create an analyzer for the endpoint
            analyzer = EndpointAnalyzer(endpoint_class, parameter_store=parameter_store)
            analyzer.set_pause_time(pause)
            
            # Analyze the endpoint
            result = analyzer.analyze()
            
            # Save the result
            results[name] = result
            
            # Update the parameter store
            parameter_store.update_from_analysis(name, result)
            
            # Print the result status
            print(f"  Status: {result['status']}")
            
            # Pause between endpoints
            time.sleep(pause)
        except Exception as e:
            print(f"  Error analyzing {name}: {e}")
            
    # Save results to file if specified
    if output_file:
        with open(output_file, 'w') as f:
            json.dump(results, f, indent=2)
            
    return results


def analyze_endpoint_with_retry(endpoint_name, retry_attempts=3, pause=1):
    """
    Analyze a single endpoint with retries.
    
    Args:
        endpoint_name: Name of the endpoint to analyze
        retry_attempts: Number of retry attempts
        pause: Pause time between attempts in seconds
    
    Returns:
        dict: Analysis results or None if all attempts failed
    """
    attempt = 0
    while attempt < retry_attempts:
        attempt += 1
        try:
            # Create an analyzer for the endpoint
            analyzer = EndpointAnalyzer(endpoint_name)
            analyzer.set_pause_time(pause)
            
            # Analyze the endpoint
            return analyzer.analyze()
        except Exception as e:
            print(f"Attempt {attempt} failed: {e}")
            time.sleep(pause)
            
    print(f"Failed to analyze {endpoint_name} after {retry_attempts} attempts")
    return None


def main():
    """Main entry point for the CLI."""
    parser = argparse.ArgumentParser(description='NBA API Endpoint Analyzer')
    parser.add_argument('--endpoint', help='Name of the endpoint to analyze')
    parser.add_argument('--all', action='store_true', help='Analyze all endpoints')
    parser.add_argument('--list', action='store_true', help='List all available endpoints')
    parser.add_argument('--output', help='Output file path')
    parser.add_argument('--pause', type=float, default=1, help='Pause between API calls in seconds')
    parser.add_argument('--retry', type=int, default=3, help='Number of retry attempts')
    
    args = parser.parse_args()
    
    # Discover available endpoints
    endpoints = discover_endpoints_from_files()
    
    if args.list:
        print(f"Available endpoints ({len(endpoints)}):")
        for name in sorted(endpoints.keys()):
            print(f"  - {name}")
        return 0
        
    if args.endpoint:
        if args.endpoint not in endpoints:
            print(f"Error: Endpoint '{args.endpoint}' not found")
            print("Use --list to see available endpoints")
            return 1
            
        print(f"Analyzing {args.endpoint}...")
        result = analyze_endpoint_with_retry(
            args.endpoint, 
            retry_attempts=args.retry,
            pause=args.pause
        )
        
        if result:
            if args.output:
                with open(args.output, 'w') as f:
                    json.dump({args.endpoint: result}, f, indent=2)
            else:
                print(json.dumps(result, indent=2))
        
        return 0
        
    if args.all:
        print(f"Analyzing all {len(endpoints)} endpoints...")
        results = analyze_all_endpoints(
            endpoints=endpoints,
            pause=args.pause,
            output_file=args.output
        )
        
        # Print summary
        success_count = sum(1 for r in results.values() if r["status"] == "success")
        deprecated_count = sum(1 for r in results.values() if r["status"] == "deprecated")
        invalid_count = sum(1 for r in results.values() if r["status"] == "invalid")
        
        print("\nAnalysis Summary:")
        print(f"  Total endpoints: {len(results)}")
        print(f"  Success: {success_count}")
        print(f"  Deprecated: {deprecated_count}")
        print(f"  Invalid: {invalid_count}")
        
        if args.output:
            print(f"\nResults saved to {args.output}")
        
        return 0
        
    # If no action specified, print help
    parser.print_help()
    return 0


if __name__ == "__main__":
    sys.exit(main())
