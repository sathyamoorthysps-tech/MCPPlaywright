#!/usr/bin/env python3
"""
Run the generated CI matrix locally for debugging.

This script calls `tools/gen_matrix.py` to get matrix entries, then for each entry
it uses `tools/split_tests.py` to select tests for that shard and runs
`tools/run_pytest_and_log.py` for those tests, storing reports and logs per shard.

Usage:
  python tools/run_local_matrix.py [--headed]

"""
import json
import subprocess
import sys
from pathlib import Path
import argparse


def run_cmd(cmd):
    print("Running:", " ".join(cmd))
    rc = subprocess.call(cmd)
    return rc


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--headed", action="store_true", help="Run browsers headed")
    args = parser.parse_args()

    python = sys.executable
    # generate matrix
    gen = subprocess.check_output([python, "tools/gen_matrix.py"])
    matrix = json.loads(gen)

    reports_dir = Path("reports")
    logs_dir = Path("logs")
    reports_dir.mkdir(exist_ok=True)
    logs_dir.mkdir(exist_ok=True)

    failures = []
    for entry in matrix:
        browser = entry.get("browser")
        shard = entry.get("shard")
        total = entry.get("total_shards")
        print(f"\n=== Running shard {shard}/{total} on {browser} ===")

        # select tests for this shard
        sel = subprocess.check_output([python, "tools/split_tests.py", "--shard", str(shard), "--total", str(total)])
        tests = sel.decode().strip()
        if not tests:
            print("No tests for this shard, skipping")
            continue

        # build report and html paths
        junit = reports_dir / f"junit-{browser}-shard-{shard}.xml"
        html = reports_dir / f"html-{browser}-shard-{shard}.html"

        cmd = [python, "tools/run_pytest_and_log.py", "-q", "-n", "auto"]
        cmd += tests.split()
        cmd += ["--browser", browser, "--junitxml", str(junit), "--html", str(html)]
        if args.headed:
            cmd.append("--headed")

        rc = run_cmd(cmd)
        if rc != 0:
            failures.append((browser, shard, rc))

    if failures:
        print("\nSome shards failed:")
        for b, s, rc in failures:
            print(f" - {b} shard {s}: exit {rc}")
        sys.exit(1)
    print("\nAll shards completed successfully")


if __name__ == "__main__":
    main()
