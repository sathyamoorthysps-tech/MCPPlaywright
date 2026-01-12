#!/usr/bin/env python3
"""
Run pytest with given arguments, stream console output and save it to a timestamped log file.

Usage:
  python tools/run_pytest_and_log.py [pytest args]

Example:
  python tools/run_pytest_and_log.py -q -s --browser=chromium --headed -k iphone
"""
import sys
import subprocess
from datetime import datetime
from pathlib import Path


def main():
    args = sys.argv[1:]
    logs_dir = Path("logs")
    logs_dir.mkdir(exist_ok=True)
    ts = datetime.now().strftime("%Y%m%d-%H%M%S")
    logfile = logs_dir / f"pytest-{ts}.log"

    cmd = [sys.executable, "-m", "pytest"] + args
    print(f"Running: {' '.join(cmd)}")
    print(f"Logging to: {logfile}")

    with logfile.open("w", encoding="utf-8") as fh:
        proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
        assert proc.stdout is not None
        try:
            for line in proc.stdout:
                print(line, end="")
                fh.write(line)
        except KeyboardInterrupt:
            proc.terminate()
            proc.wait()
            raise
        rc = proc.wait()

    print(f"Pytest finished with exit code {rc}. Log saved to {logfile}")
    sys.exit(rc)


if __name__ == "__main__":
    main()
