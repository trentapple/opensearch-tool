# opensearch-tool
A tools implementation for OpenSearch use in SOC environments such as with SecurityOnion / Elasticsearch.

<details><summary>Roadmap</summary>

| Phase | Core Focus | Key Deliverables |
|-------|------------|------------------|
| **Immediate** | • Core query API – field selection, default `@timestamp` sorting, comprehensive pagination limits, validation | • `fields` parameter<br>• Enhanced options for default sort logic<br>• Size guard & robust error handling |
| **Short‑Term** | • Developer tooling – documentation | • README + quick‑start guide<br>• GitHub Actions (lint, tests, packaging) |
| **Mid‑Term** | • Performance & security – caching capabilities, adaptive rate‑limit handling, extensibility, advanced authentication | • In‑memory cache module<br>• Auth plug‑in (currently supports **API Bearer Token** and **Basic Auth**; future work: OIDC/OAuth)<br>• Back‑off strategy, structured logging |
| **Long‑Term** | • Advanced functionality – multi‑cluster orchestration, aggregations, optional UI | • Multi‑cluster query support<br>• Aggregation helpers<br>• Prototype user interface |
</details>
