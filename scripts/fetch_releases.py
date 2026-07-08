#!/usr/bin/env python3
"""Fetch the latest GitHub release for tracked Hermes repos and write data/releases.json."""
import json
import os
import urllib.request
import urllib.error

REPOS = [
    "NousResearch/hermes-agent",
    "NousResearch/Hermes-Function-Calling",
]
API = "https://api.github.com/repos/{}/releases/latest"
OUT = os.path.join(os.path.dirname(__file__), "..", "data", "releases.json")

HEADERS = {"User-Agent": "awesome-hermes-tracker", "Accept": "application/vnd.github+json"}


def fetch(repo):
    req = urllib.request.Request(API.format(repo), headers=HEADERS)
    try:
        with urllib.request.urlopen(req, timeout=20) as r:
            data = json.load(r)
    except urllib.error.HTTPError as e:
        if e.code == 404:
            return {"latest_tag": None, "published_at": None, "url": None}
        raise
    return {
        "latest_tag": data.get("tag_name"),
        "published_at": data.get("published_at"),
        "url": data.get("html_url"),
    }


def main():
    result = {
        "updated_at": __import__("datetime").datetime.now(
            __import__("datetime").timezone.utc
        ).isoformat(),
        "repos": {repo: fetch(repo) for repo in REPOS},
    }
    out_path = os.path.abspath(OUT)
    with open(out_path, "w") as f:
        json.dump(result, f, indent=2)
        f.write("\n")
    print("Wrote", out_path)
    for repo, info in result["repos"].items():
        print(f"  {repo}: {info['latest_tag']}")


if __name__ == "__main__":
    main()
