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
playwright install
```

3. Run the BDD tests:

```powershell
pytest -q
```

Notes
- The sample BDD feature searches on https://www.amazon.in using a single scenario.
- CI is configured via GitHub Actions in `.github/workflows/ci.yml`.

CI runs tests in a browser matrix (`chromium`, `firefox`, `webkit`) and retries failed tests up to 2 times to reduce flakiness.

We also support two parallelization options:
- Intra-run parallelism using `pytest-xdist` (`pytest -n auto`) to run tests across multiple processes on a single runner.
- Horizontal sharding across multiple GitHub Actions jobs using a simple splitter script (`tools/split_tests.py`) which divides test files evenly across shards.

Both strategies are enabled in CI: `test-xdist` (xdist) and `sharded-tests` (parallel shards). CI now also caches Playwright browser artifacts to speed subsequent runs and uploads JUnit and HTML reports as job artifacts.

Matrix parallelism tuning
- The `sharded-tests` job is pre-configured for `TOTAL_SHARDS` values of 2 and 4. Each combination of `browser` and `shard` is enumerated in the matrix.
- `strategy.max-parallel` is set to 6 to limit concurrent shard jobs; adjust this value in `.github/workflows/ci.yml` to tune concurrency vs CI minutes.

To add more shards, edit the matrix `include` section in `.github/workflows/ci.yml` and add entries for the desired `total_shards` and shard indices.

Dynamic generation: a small helper `tools/gen_matrix.py` generates the matrix JSON used by CI. Update that script to change browsers or shard counts instead of editing YAML manually.

If you want me to run tests locally or customize browsers/timeout, tell me which browser to target (chromium, firefox, or webkit).
