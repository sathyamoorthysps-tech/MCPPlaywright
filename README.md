MCP Playwright Python — BDD setup for Amazon.in

This repository scaffolds Playwright for Python with a BDD workflow (pytest-bdd) and a GitHub Actions CI to run tests.

Quick start

1. Create and activate a virtualenv (Windows example):

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

2. Install dependencies:

```powershell
pip install -r requirements.txt
**MCP Playwright Python — BDD test scaffold**

This repository demonstrates a Playwright + pytest BDD setup (pytest-bdd) with helper scripts for local runs and a CI workflow that shards tests across a browser matrix.

**Quick setup**

- Create and activate a virtual environment (Windows):

	```powershell
	python -m venv .venv
	.\.venv\Scripts\Activate.ps1
	```

- Install Python dependencies and Playwright browsers:

	```powershell
	pip install -r requirements.txt
	python -m playwright install chromium firefox webkit
	```

	Note: on CI (Ubuntu) you should install Playwright system libraries before running `python -m playwright install`. For example:

	```bash
	sudo apt-get update && sudo apt-get install -y \
		libnss3 libatk1.0-0 libatk-bridge2.0-0 libx11-xcb1 libxcomposite1 libxdamage1 \
		libxrandr2 libgbm1 libasound2 libpangocairo-1.0-0 libgtk-3-0 libxshmfence1 libcups2
	```

**Run tests locally**

- Run directly with pytest:

	```powershell
	pytest -q
	```

- Or use the provided test wrapper (captures logs in `logs/`):

	```powershell
	.\.venv\Scripts\python.exe tools\run_pytest_and_log.py -q -s --browser=chromium --headed
	```

	The wrapper outputs logs to `logs/pytest-<timestamp>.log` and mirrors pytest output to the console.

**Parallelization & sharding**

- Intra-run parallelism: use `pytest -n auto` (requires `pytest-xdist`).
- Horizontal sharding: `tools/split_tests.py` divides test files into shards. Example (shard 0 of 2):

	```powershell
	$TESTS = python tools/split_tests.py --shard 0 --total 2
	.\.venv\Scripts\python.exe tools\run_pytest_and_log.py -q -s -n auto $TESTS --browser=chromium --headed
	```

**CI notes**

- The GitHub Actions workflow is at `.github/workflows/ci.yml`. It runs a browser matrix (`chromium`, `firefox`, `webkit`) and shards tests across jobs. The workflow installs system packages required by Playwright on Ubuntu, caches pip and Playwright browser artifacts, and runs `python -m playwright install <browser>` per matrix entry.
- To speed up CI, we've removed duplicate pip installs and added apt package installation prior to `playwright install`.

**Project layout & helper scripts**

- `tests/` — BDD features and step implementations. The Page Object `tests/pages/search_page.py` centralizes locators and actions.
- `tools/run_pytest_and_log.py` — wrapper to run pytest and save logs.
- `tools/split_tests.py` — simple test splitter for sharding across CI jobs.
- `tools/gen_matrix.py` — helper to generate the GitHub Actions matrix JSON for shards and browsers.

**Troubleshooting & tips**

- If tests fail due to missing system libraries on CI, ensure the apt list above is installed before `python -m playwright install`.
- If Playwright browsers are not found locally, run `python -m playwright install chromium` (or `firefox`/`webkit`).
- Use `-k <expr>` with pytest to run a subset of tests by keyword.

If you want, I can:
- open a PR with these README and requirements changes,
- remove any leftover temporary test files (e.g., `test_search_clean.py`) and confirm repository cleanliness, or
- push CI workflow to a branch and run CI remotely.
