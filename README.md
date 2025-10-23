# opensearch-tool

SecurityOnionTools – a thin wrapper around the opensearch-py client
that knows the "so-*" or "logs-*" index pattern used by Security Onion.

**requirements:** opensearch-py

## Overview

This is a tools implementation for OpenSearch use in SOC environments such as with Security Onion / Elasticsearch. The tool provides a streamlined interface for querying and interacting with Security Onion's OpenSearch indices.

## About Open WebUI Tools

This tool is designed for use with Open WebUI tools, enabling LLMs (Large Language Models) to interact with Security Onion data. Similar to MCP (Model Context Protocol), it provides a structured way for AI assistants to query security logs and indices.

The implementation follows the Open WebUI Tools pattern with:
- **Tools class**: Main interface for LLM integration
- **Valves**: Pydantic-based configuration that can be adjusted at runtime
- **Async operations**: Non-blocking queries for better performance
- **Citation support**: Results can be traced back to their source

## Features

- Automatic detection of Security Onion index patterns (`so-*` and `logs-*`)
- Simplified wrapper around opensearch-py for security operations
- Compatible with Open WebUI tools for LLM integration
- Easy integration with Security Onion environments

## Requirements

- opensearch-py
- pydantic

## Installation

```bash
pip install opensearch-py pydantic
```

## Configuration

The tool uses a `Valves` configuration system for flexible deployment:

- **host**: OpenSearch host (default: "securityonion")
- **port**: OpenSearch port (default: 9200)
- **username/password**: Basic authentication credentials
- **api_key**: Bearer token for API-Key authentication
- **use_ssl**: Enable HTTPS (default: True)
- **verify_certs**: Verify TLS certificates (default: True)
- **default_index**: Default index pattern (default: "so-*")
- **request_timeout**: Request timeout in seconds (default: 60)

## Usage

The tool provides a `soc_query` method that automatically handles Security Onion specific index patterns:

```python
# Execute a query against Security Onion indices
result = await tools.soc_query(
    query_string="event.severity:critical AND host.name:webserver",
    size=20
)
```

The tool automatically:
- Detects and uses appropriate indices (so-*, logs-*)
- Handles authentication (basic auth or API key)
- Manages SSL/TLS connections
- Sorts results by @timestamp (most recent first)

## License

See LICENSE file for details.
