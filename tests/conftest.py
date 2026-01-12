import re
from pathlib import Path


def _sanitize(name: str) -> str:
    s = re.sub(r"[^0-9a-zA-Z]+", "_", name).strip("_").lower()
    return s


def pytest_collection_modifyitems(config, items):
    # Build mapping from sanitized scenario base -> (feature_path, scenario_name)
    mapping = {}
    features_dir = Path(config.rootpath) / "tests" / "features"
    if features_dir.exists():
        for f in features_dir.rglob("*.feature"):
            try:
                text = f.read_text(encoding="utf-8")
            except Exception:
                continue
            for line in text.splitlines():
                line = line.strip()
                if line.startswith("Scenario:"):
                    scenario = line.split("Scenario:", 1)[1].strip()
                    key = _sanitize(scenario)
                    mapping[key] = (str(f.relative_to(config.rootpath)), scenario)

    for item in items:
        # Preserve original pytest item name (e.g. 'test_search_for_a_product')
        orig_name = getattr(item, "name", "")
        base = orig_name
        if base.startswith("test_"):
            base = base[5:]
        key = base.lower()
        if key in mapping:
            feature_path, scenario_name = mapping[key]
            # Set a friendlier nodeid and name for Test Explorer, include original test name
            try:
                combined = f"{feature_path}::{scenario_name} ({orig_name})"
                item._nodeid = combined
                item.name = f"{scenario_name} ({orig_name})"
            except Exception:
                # best-effort; ignore failures
                pass