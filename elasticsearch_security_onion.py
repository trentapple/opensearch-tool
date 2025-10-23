"""
SecurityOnionTools – a thin wrapper around the opensearch‑py client
that knows the "so-*" or "logs-*" index pattern used by Security Onion.
requirements: opensearch-py
"""

import asyncio
import logging
from datetime import datetime, timedelta
from typing import Any, Dict, Optional, List

from opensearchpy import AsyncOpenSearch, NotFoundError
from pydantic import BaseModel, Field


class Tools:
    class Valves(BaseModel):
        host: str = Field(default="securityonion", description="OpenSearch host.")
        port: int = Field(default=9200, description="OpenSearch port.")
        username: Optional[str] = Field(
            default=None, description="Basic auth username."
        )
        password: Optional[str] = Field(
            default=None, description="Basic auth password."
        )
        api_key: Optional[str] = Field(
            default=None, description="Bearer token for API‑Key authentication."
        )
        use_ssl: bool = Field(default=True, description="Use HTTPS.")
        verify_certs: bool = Field(default=True, description="Verify TLS certs.")
        default_index: str = Field(default="so-*", description="Default index pattern.")
        request_timeout: int = Field(
            default=60, description="Seconds to wait for a response."
        )

    def __init__(self):
        self.valves = self.Valves()
        # NOTE: No persistent `client` attribute – each call creates its own client.
        self.citation = True

    # ------------------------------------------------------------------
    # Core search API – all helpers are local to this method
    # ------------------------------------------------------------------
    async def soc_query(
        self,
        query_string: str,
        # index: str = "*",
        size: int = 20,
        sort: Optional[List[Dict[str, Any]]] = None,
    ) -> Dict[str, Any]:
        """
        Execute a custom SOC query against the "so-*" index pattern.

        Parameters
        ----------
        query_string : str
            The raw query string (query_string) that will be wrapped in the
            OpenSearch DSL `query_string` clause.
        size : int, optional
            Number of hits to return (default 20).
        index : str, default "*"
            Index or index pattern with wildcard(s) to utilize.
        sort : list[dict], optional
            Explicit sort specification. If omitted, results are sorted by
            ``@timestamp`` descending (i.e., most recent first).

        Returns
        -------
        dict
            Full OpenSearch response.
        """
        index = None

        def _setup_client() -> AsyncOpenSearch:
            scheme = "https" if self.valves.use_ssl else "http"
            es_url = f"{scheme}://{self.valves.host}:{self.valves.port}"
            auth = (
                (self.valves.username, self.valves.password)
                if self.valves.username and self.valves.password
                else None
            )
            headers: Dict[str, str] = {}
            if self.valves.api_key:
                headers["Authorization"] = f"ApiKey {self.valves.api_key}"
            return AsyncOpenSearch(
                hosts=[es_url],
                http_auth=auth,
                headers=headers,
                use_ssl=self.valves.use_ssl,
                verify_certs=self.valves.verify_certs,
                timeout=self.valves.request_timeout,
            )

        # ------------------------------------------------------------------
        # Helper: resolve a concrete index name from a pattern
        # ------------------------------------------------------------------
        async def _ensure_index(idx: str) -> str:
            if idx:
                return idx
            try:
                indices = await client.indices.get_alias("*")
                for name in indices:
                    if name.startswith("so-"):
                        return name
                    elif "so" in name:
                        return name
                    elif "logs" in name:
                        return name
                    else:
                        return "*"
                raise ValueError("No suitable index found.")
            except Exception as exc:
                logging.error(f"Index resolution error: {exc}")
                raise

        def _build_body(body_query: Dict[str, Any], sz: int = 10) -> Dict[str, Any]:
            return {"query": body_query, "size": sz}

        client = _setup_client()
        try:
            idx = await _ensure_index(index or self.valves.default_index)
            body = {
                "query": {"query_string": {"query": query_string}},
                # "sort": sort or [{"@timestamp": {"order": "desc"}}],
            }
            return await client.search(index=idx, body=body, size=size)
        except Exception as exc:
            logging.error(f"Soc query failed: {exc}")
            raise
        finally:
            await client.close()
