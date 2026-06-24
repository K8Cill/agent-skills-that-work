#!/usr/bin/env python3
"""Validate the plugin metadata so `/plugin install` never breaks.

Checks:
  - .claude-plugin/plugin.json and marketplace.json are valid JSON
  - plugin.json has name + version
  - marketplace.json has name + plugins array
  - each plugin entry has name + source
  - source paths resolve inside the repo (no path traversal)
"""
import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PLUGIN_DIR = os.path.join(ROOT, ".claude-plugin")


def load_json(path):
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def main():
    errors = []

    plugin_path = os.path.join(PLUGIN_DIR, "plugin.json")
    market_path = os.path.join(PLUGIN_DIR, "marketplace.json")

    for p in (plugin_path, market_path):
        if not os.path.isfile(p):
            errors.append(f"missing {os.path.relpath(p, ROOT)}")

    if errors:
        print("Manifest validation FAILED:\n")
        for e in errors:
            print(f"  - {e}")
        sys.exit(1)

    try:
        plugin = load_json(plugin_path)
    except json.JSONDecodeError as e:
        errors.append(f"plugin.json invalid JSON: {e}")
        plugin = {}
    try:
        market = load_json(market_path)
    except json.JSONDecodeError as e:
        errors.append(f"marketplace.json invalid JSON: {e}")
        market = {}

    if plugin and not plugin.get("name"):
        errors.append("plugin.json missing 'name'")
    if plugin and not plugin.get("version"):
        errors.append("plugin.json missing 'version'")

    if market:
        if not market.get("name"):
            errors.append("marketplace.json missing 'name'")
        plugins = market.get("plugins")
        if not isinstance(plugins, list) or not plugins:
            errors.append("marketplace.json missing non-empty 'plugins' array")
        else:
            for idx, entry in enumerate(plugins):
                if not entry.get("name"):
                    errors.append(f"plugins[{idx}] missing 'name'")
                src = entry.get("source")
                if not src:
                    errors.append(f"plugins[{idx}] missing 'source'")
                elif ".." in str(src):
                    errors.append(f"plugins[{idx}] source '{src}' escapes repo (path traversal)")

    if errors:
        print("Manifest validation FAILED:\n")
        for e in errors:
            print(f"  - {e}")
        sys.exit(1)
    print("Manifest validation passed: plugin.json + marketplace.json OK.")


if __name__ == "__main__":
    main()
