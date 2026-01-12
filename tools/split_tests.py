#!/usr/bin/env python3
"""
Simple test splitter: lists test files under `tests/` and selects files for a shard.

Usage: python tools/split_tests.py --shard 0 --total 2
Prints matching test file paths separated by spaces.
"""
import argparse
from pathlib import Path
import sys


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--shard", type=int, required=True)
    parser.add_argument("--total", type=int, required=True)
    args = parser.parse_args()

    tests_dir = Path("tests")
    if not tests_dir.exists():
        print("", end="")
        return

    files = sorted([str(p) for p in tests_dir.rglob("test_*.py")])
    selected = [f for i, f in enumerate(files) if (i % args.total) == args.shard]

    if selected:
        print(" ".join(selected))
    else:
        # print nothing if no tests assigned to this shard
        print("", end="")


if __name__ == "__main__":
    main()
