#!/usr/bin/env python3
"""
NextDNS Multi-Profile & Multi-Category Automated Blocklist Synchronizer

Features:
- Multi-Profile Support: Sync across multiple NextDNS profile IDs in a single run.
- Category Selection: Choose any category (streaming, gaming, torrenting, etc.) or "all".
- Smart Delta Sync: Only pushes new domains (0 API spam on subsequent runs).
- Rate Limit Resilience: Automatic retry with exponential backoff on HTTP 429 / 5xx.
- ThreadPool Concurrency: Fast parallel uploads while staying within NextDNS API limits.
- Personal Rule Protection: Preserves personal custom rules on NextDNS.
"""

import os
import sys
import time
import argparse
from concurrent.futures import ThreadPoolExecutor, as_completed
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

NEXTDNS_API_BASE = "https://api.nextdns.io/profiles"

# Category file mapping (reads from local repo lists/hosts/)
CATEGORY_FILES = {
    "all": "lists/hosts/all.txt",
    "streaming": "lists/hosts/streaming.txt",
    "gaming": "lists/hosts/gaming.txt",
    "audio": "lists/hosts/audio.txt",
    "reading": "lists/hosts/reading.txt",
    "downloading": "lists/hosts/downloading.txt",
    "torrenting": "lists/hosts/torrenting.txt",
    "mobile": "lists/hosts/mobile.txt",
    "ai": "lists/hosts/ai.txt",
    "non_english": "lists/hosts/non_english.txt"
}

def create_resilient_session(api_key):
    """Creates a requests session with retry backoff for rate limits (HTTP 429)."""
    session = requests.Session()
    retries = Retry(
        total=5,
        backoff_factor=1.5,
        status_forcelist=[429, 500, 502, 503, 504],
        raise_on_status=False
    )
    adapter = HTTPAdapter(max_retries=retries, pool_connections=10, pool_maxsize=10)
    session.mount("https://", adapter)
    session.headers.update({
        "X-Api-Key": api_key,
        "Content-Type": "application/json",
        "User-Agent": "NextDNS-FMHY-Sync/1.0"
    })
    return session

def load_target_domains(selected_categories):
    """Loads and deduplicates target domains from selected categories."""
    target_domains = set()
    categories = [c.strip().lower() for c in selected_categories.split(",") if c.strip()]
    
    if "all" in categories:
        categories = ["all"]

    for cat in categories:
        filepath = CATEGORY_FILES.get(cat)
        if not filepath or not os.path.exists(filepath):
            print(f"[!] Warning: Category '{cat}' file not found at {filepath}, skipping.")
            continue
            
        print(f"[+] Ingesting category '{cat}' from {filepath}...")
        with open(filepath, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith("#") or line.startswith("!"):
                    continue
                parts = line.split()
                domain = parts[-1] if parts else line
                domain = domain.lower()
                if domain not in ["127.0.0.1", "0.0.0.0", "localhost"]:
                    target_domains.add(domain)

    return target_domains

def get_current_denylist(session, profile_id):
    """Fetches all domains currently present in the profile's Denylist."""
    url = f"{NEXTDNS_API_BASE}/{profile_id}/denylist"
    res = session.get(url, timeout=15)
    if res.status_code == 200:
        data = res.json().get("data", [])
        return {item["id"].lower() for item in data if "id" in item}
    elif res.status_code == 404:
        print(f"[!] Profile ID '{profile_id}' not found. Please verify profile ID.")
        return None
    elif res.status_code in [401, 403]:
        print(f"[!] Authentication error. Please verify NEXTDNS_API_KEY.")
        return None
    else:
        print(f"[!] Error fetching denylist for profile {profile_id}: HTTP {res.status_code} - {res.text}")
        return None

def add_single_domain(session, profile_id, domain):
    """Pushes a single domain to NextDNS denylist with rate-limit safety."""
    url = f"{NEXTDNS_API_BASE}/{profile_id}/denylist"
    payload = {"id": domain, "active": True}
    try:
        res = session.post(url, json=payload, timeout=10)
        if res.status_code in [200, 201]:
            return True, domain
        elif res.status_code == 429:
            time.sleep(2)
            res = session.post(url, json=payload, timeout=10)
            return res.status_code in [200, 201], domain
        else:
            return False, f"{domain} (HTTP {res.status_code}: {res.text})"
    except Exception as e:
        return False, f"{domain} (Exception: {e})"

def sync_profile(session, profile_id, target_domains, max_workers=5):
    """Synchronizes target domains to a specific NextDNS profile."""
    print(f"\n{'='*60}")
    print(f"[*] Starting Sync for Profile ID: {profile_id}")
    print(f"{'='*60}")
    
    current_domains = get_current_denylist(session, profile_id)
    if current_domains is None:
        return False

    print(f"[i] Profile {profile_id}: Currently has {len(current_domains)} rules in NextDNS.")
    
    # Delta calculation: only add newcomer domains
    to_add = sorted(target_domains - current_domains)
    
    if not to_add:
        print(f"[✓] Profile {profile_id}: 100% up to date! Zero new domains to add.")
        return True

    print(f"[+] Found {len(to_add)} new domains to add to Profile {profile_id}...")

    success_count = 0
    fail_count = 0
    failed_details = []

    # Push with controlled concurrency
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = {executor.submit(add_single_domain, session, profile_id, domain): domain for domain in to_add}
        for idx, future in enumerate(as_completed(futures), 1):
            ok, result = future.result()
            if ok:
                success_count += 1
            else:
                fail_count += 1
                failed_details.append(result)
            
            if idx % 100 == 0 or idx == len(to_add):
                print(f"    -> Progress: {idx}/{len(to_add)} processed ({success_count} succeeded, {fail_count} failed)")

    print(f"\n[✓] Profile {profile_id} Sync Completed:")
    print(f"    - Added: {success_count}")
    print(f"    - Failed: {fail_count}")
    print(f"    - Total Active in NextDNS: {len(current_domains) + success_count}")

    if failed_details:
        print(f"    - First few failures: {failed_details[:5]}")

    return True

def main():
    parser = argparse.ArgumentParser(description="Sync FMHY blocklists to NextDNS Denylist.")
    parser.add_argument("--categories", default=os.environ.get("NEXTDNS_CATEGORIES", "streaming"),
                        help="Comma-separated categories to sync (e.g. 'streaming', 'gaming,torrenting', or 'all')")
    parser.add_argument("--profiles", default=os.environ.get("NEXTDNS_PROFILES", os.environ.get("NEXTDNS_PROFILE", "")),
                        help="Comma-separated NextDNS Profile IDs (e.g. 'a1b2c3,d4e5f6')")
    parser.add_argument("--api-key", default=os.environ.get("NEXTDNS_API_KEY", ""),
                        help="NextDNS API Key from Account page")
    parser.add_argument("--workers", type=int, default=5,
                        help="Concurrent worker threads (default 5)")
    args = parser.parse_args()

    api_key = args.api_key.strip()
    profiles_str = args.profiles.strip()
    categories_str = args.categories.strip()

    if not api_key:
        print("[CRITICAL] Missing NextDNS API Key. Set NEXTDNS_API_KEY environment variable or pass --api-key.")
        sys.exit(1)

    if not profiles_str:
        print("[CRITICAL] Missing NextDNS Profile IDs. Set NEXTDNS_PROFILES environment variable or pass --profiles.")
        sys.exit(1)

    profiles = [p.strip() for p in profiles_str.split(",") if p.strip()]
    
    print("="*60)
    print("NextDNS Multi-Profile & Multi-Category Synchronizer")
    print("="*60)
    print(f"Target Profiles : {profiles}")
    print(f"Categories      : {categories_str}")
    print(f"Worker Threads  : {args.workers}")
    print("="*60)

    # 1. Load target domains
    target_domains = load_target_domains(categories_str)
    if not target_domains:
        print("[!] No target domains found. Exiting.")
        sys.exit(1)

    print(f"[+] Total unique target rules to enforce: {len(target_domains):,}")

    # 2. Sync to all profiles sequentially
    session = create_resilient_session(api_key)
    overall_success = True
    for profile_id in profiles:
        ok = sync_profile(session, profile_id, target_domains, max_workers=args.workers)
        if not ok:
            overall_success = False

    print(f"\n{'='*60}")
    if overall_success:
        print("[SUCCESS] All profiles synced successfully with NextDNS!")
    else:
        print("[WARNING] One or more profiles encountered errors during sync.")
    print("="*60)

if __name__ == "__main__":
    main()
