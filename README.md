# opensearch-tool

SecurityOnionTools – a thin wrapper around the opensearch-py client
that knows the "so-*" or "logs-*" index pattern used by Security Onion.

**requirements:** opensearch-py

## Overview

This is a tools implementation for OpenSearch use in SOC environments such as with Security Onion / Elasticsearch. The tool provides a streamlined interface for querying and interacting with Security Onion's OpenSearch indices.

## About Open WebUI Tools

This tool is designed for use with Open WebUI tools, enabling LLMs (Large Language Models) to interact with Security Onion data. Similar to MCP (Model Context Protocol), it provides a structured way for AI assistants to query security logs and indices.

## Features

- Automatic detection of Security Onion index patterns (`so-*` and `logs-*`)
- Simplified wrapper around opensearch-py for security operations
- Compatible with Open WebUI tools for LLM integration
- Easy integration with Security Onion environments

## Requirements

- opensearch-py

## Usage

The tool provides a thin wrapper that automatically handles the Security Onion specific index patterns, making it easier to query security logs without manually specifying index names.

## License

See LICENSE file for details.
