# Project Roadmap

- **Stabilize CLI experience**  
  Deliver consistent plain-text output, add `--json`/`--yaml` formats, and ensure exit codes signal success or failure for scripting workflows.

- **Expand GitHub insights**  
  Fetch richer repository data such as latest releases, default branch, open pull requests, and popularity metrics; explore batch lookups (`owner/repo repo2 …`).

- **Improve resilience**  
  Introduce retry/backoff for rate limits, clearer 403/404 guidance, configurable timeouts, and optional logging hooks for debugging.

- **Grow test coverage**  
  Add integration tests against a mocked GitHub API, snapshot tests for new output formats, and cases covering non-ASCII repos and network failures.

- **Polish packaging and docs**  
  Align branding across README/PyPI, publish changelog and contribution guidelines, and enrich docs with badges, screenshots, and advanced usage examples.

- **Automate delivery**  
  Configure CI (e.g., GitHub Actions) for linting, typing, tests, and PyPI publishing; add checks for `uv.lock` drift.

- **Explore future directions**  
  Prototype a lightweight web dashboard or TUI, expose a reusable Python API, and triage community feedback into future iterations.
