#!/usr/bin/env python3
"""
Generate a JSON array for GitHub Actions matrix 'include' entries.

Usage: python tools/gen_matrix.py
Prints a JSON array to stdout, e.g.:
[{"browser":"chromium","shard":0,"total_shards":2}, ...]

You can customize browsers and shard_counts below.
"""
import json


def generate(browsers=None, shard_counts=None):
    if browsers is None:
        browsers = ["chromium", "firefox", "webkit"]
    if shard_counts is None:
        shard_counts = [2, 4]

    arr = []
    for total in shard_counts:
        for browser in browsers:
            for shard in range(total):
                arr.append({"browser": browser, "shard": shard, "total_shards": total})
    return arr


def main():
    matrix = generate()
    print(json.dumps(matrix))


if __name__ == "__main__":
    main()
