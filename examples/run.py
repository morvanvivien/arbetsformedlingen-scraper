"""Minimal example: run the arbetsformedlingen-jobs-scraper Actor and print the results.

Usage: APIFY_TOKEN=... python run.py   (pip install apify-client)
"""
import os
import sys

from apify_client import ApifyClient

token = os.environ.get("APIFY_TOKEN")
if not token:
    sys.exit("Set the APIFY_TOKEN environment variable first.")

client = ApifyClient(token)

run_input = {
    "keyword": "sjukskoterska",
    "maxItems": 50,
}

run = client.actor("bibian/arbetsformedlingen-jobs-scraper").call(run_input=run_input)

count = 0
for item in client.dataset(run.default_dataset_id).iterate_items():
    count += 1
    employer = item.get("employer") or {}
    print(f"{item['title']} | {employer.get('name')} | {item.get('municipality')}")
print(f"{count} results")
