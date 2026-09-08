import os
import re
import sys
import datetime
from concurrent.futures import ThreadPoolExecutor
from urllib.parse import urlparse
import requests

# Multi-mirror endpoints for robust failover
# If GitHub Raw is down or blocked, falls back to jsDelivr CDN and GitLab
MIRROR_TEMPLATES = [
    "https://raw.githubusercontent.com/fmhy/edit/main/docs/{filename}",
    "https://cdn.jsdelivr.net/gh/fmhy/edit@main/docs/{filename}",
    "https://gitlab.com/vvispy/fmhy/-/raw/main/docs/{filename}"
]

# Upstream category markdown files and output list metadata
CATEGORIES = {
    "streaming": {
        "file": "video.md",
        "output": "streaming.txt",
        "title": "FMHY Movies & TV Streaming Blocklist",
        "description": "Movies, TV shows, anime, cartoon, sports streaming, and video aggregators."
    },
    "gaming": {
        "file": "gaming.md",
        "output": "gaming.txt",
        "title": "FMHY Gaming Blocklist",
        "description": "Pirated games, ROMs, ISOs, game repacks, cracks, and emulators."
    },
    "audio": {
        "file": "audio.md",
        "output": "audio.txt",
        "title": "FMHY Music & Audio Blocklist",
        "description": "Music streaming, lossless downloads, rippers, podcasts, and audiobooks."
    },
    "reading": {
        "file": "reading.md",
        "output": "reading.txt",
        "title": "FMHY Books & Comics Blocklist",
        "description": "E-books, textbooks, comics, manga, light novels, and magazines."
    },
    "downloading": {
        "file": "downloading.md",
        "output": "downloading.txt",
        "title": "FMHY Direct Downloads Blocklist",
        "description": "Direct download (DDL) portals, file lockers, premium debrid services."
    },
    "torrenting": {
        "file": "torrenting.md",
        "output": "torrenting.txt",
        "title": "FMHY Torrents Blocklist",
        "description": "Public & private torrent trackers, indexers, and P2P search engines."
    },
    "mobile": {
        "file": "mobile.md",
        "output": "mobile.txt",
        "title": "FMHY Mobile Piracy Blocklist",
        "description": "Modded Android APKs, sideloading stores, iOS IPA repositories."
    },
    "ai": {
        "file": "ai.md",
        "output": "ai.txt",
        "title": "FMHY Artificial Intelligence Blocklist",
        "description": "AI scrapers, unsanctioned bot mirrors, model rippers, and jailbreaks."
    },
    "non_english": {
        "file": "non-english.md",
        "output": "non_english.txt",
        "title": "FMHY International Piracy Blocklist",
        "description": "Non-English and regional piracy, streaming, and media portals."
    }
}

# Whitelist benign CDNs, tool hosts, social platforms, and documentation hubs
GLOBAL_EXCLUDES = {
    # Code & Git hosting
    "github.com", "github.io", "gitlab.com", "codeberg.org", "sourceforge.net", "bitbucket.org",
    # Communities & Social
    "reddit.com", "discord.com", "discord.gg", "twitter.com", "x.com", "t.me", "telegram.me",
    "youtube.com", "youtu.be", "twitch.tv", "instagram.com", "facebook.com", "tiktok.com",
    # Reference & Search
    "google.com", "wikipedia.org", "archive.org", "duckduckgo.com", "bing.com",
    # Funding & Donations
    "patreon.com", "ko-fi.com", "buymeacoffee.com", "paypal.com", "liberapay.com",
    # Guides, Pastes & Infrastructure
    "rentry.co", "rentry.org", "pastebin.com", "fmhy.net", "fmhy.pages.dev", "pages.dev",
    "cloudflare.com", "workers.dev", "gitbook.io", "notion.so", "notion.site",
    # Media & Image hosts
    "imgur.com", "tenor.com", "giphy.com", "ibb.co", "postimages.org"
}

# Regex to identify domain names strictly
DOMAIN_REGEX = re.compile(r'^[a-z0-9]([a-z0-9-]*[a-z0-9])?(\.[a-z0-9]([a-z0-9-]*[a-z0-9])?)+$')

def fetch_content_with_failover(filename, session):
    """Attempts to fetch markdown from primary mirror; cascades to backups on failure."""
    for mirror_url in [t.format(filename=filename) for t in MIRROR_TEMPLATES]:
        try:
            res = session.get(mirror_url, timeout=8)
            if res.status_code == 200 and len(res.text.strip()) > 500:
                print(f"  [+] Ingested {filename} from: {mirror_url} ({len(res.text)} bytes)")
                return res.text
            else:
                print(f"  [!] Mirror HTTP {res.status_code} for {mirror_url}")
        except Exception as e:
            print(f"  [!] Connection failed for {mirror_url}: {e}")
    return None

def extract_clean_domains(markdown_text):
    """Finds all Markdown and plaintext URLs and extracts unique, clean hostnames."""
    # Matches Markdown URLs [Title](https://...) and angle bracket URLs <https://...>
    raw_urls = re.findall(r'\((https?://[^)\s]+)\)', markdown_text)
    raw_urls += re.findall(r'<https?://([^>]+)>', markdown_text)
    
    domains = set()
    for link in raw_urls:
        try:
            if not link.startswith("http"):
                link = "http://" + link
            parsed = urlparse(link)
            host = parsed.netloc.lower().split(":")[0]
            
            if host.startswith("www."):
                host = host[4:]

            # Filter out invalid hosts, raw IPs, and whitelisted infrastructure
            if not host or "." not in host or host.replace(".", "").isdigit():
                continue

            if any(host == exc or host.endswith("." + exc) for exc in GLOBAL_EXCLUDES):
                continue

            if DOMAIN_REGEX.match(host):
                domains.add(host)
        except Exception:
            continue
            
    return sorted(domains)

def process_category(category_name, config, session):
    """Processes a single category: fetches upstream, extracts domains, and respects fail-safe."""
    print(f"\nProcessing category: {category_name.upper()} ({config['file']})...")
    markdown_data = fetch_content_with_failover(config["file"], session)
    output_filepath = os.path.join("lists", config["output"])
    
    # FAIL-SAFE GUARD: If all mirrors fail, preserve any pre-existing blocklist file
    if not markdown_data:
        print(f"  [CRITICAL] All mirrors failed for {category_name}. Retaining existing file to avoid empty blocklist.")
        return category_name, None

    domains = extract_clean_domains(markdown_data)
    
    # Do not overwrite if regex extracted a suspiciously small count (prevents corrupted wiki syncs)
    if len(domains) < 10:
        print(f"  [WARNING] Suspiciously low domain count ({len(domains)}). Skipping write to avoid broken list.")
        return category_name, None

    # Write out list in standard AdGuard / Adblock format (||domain^)
    with open(output_filepath, "w", encoding="utf-8") as f:
        f.write(f"! Title: {config['title']}\n")
        f.write(f"! Description: {config['description']}\n")
        f.write("! Syntax: AdGuard / Adblock Plus (||domain^)\n")
        f.write("! Generated automatically from FMHY upstream sources\n")
        f.write(f"! Total Rules: {len(domains)}\n")
        f.write(f"! Updated: {datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%d %H:%M:%S UTC')}\n\n")
        for domain in domains:
            f.write(f"||{domain}^\n")
            
    print(f"  [SUCCESS] Wrote {len(domains)} rules to {output_filepath}")
    return category_name, domains

def update_readme(category_stats, all_domains_count):
    """Generates an informative README with copyable subscription links and rule metrics."""
    username = os.environ.get("GITHUB_REPOSITORY_OWNER", "pratham-1002-adg")
    repo = os.environ.get("GITHUB_REPOSITORY", f"{username}/fmhy-blocklists").split("/")[-1]
    raw_base = f"https://raw.githubusercontent.com/{username}/{repo}/main/lists"
    cdn_base = f"https://cdn.jsdelivr.net/gh/{username}/{repo}@main/lists"
    
    now_str = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")
    
    readme_content = f"""# FMHY Multi-Category Blocklists

Automated, high-frequency AdGuard / DNS / uBlock blocklists synchronized directly from the **FreeMediaHeckYeah (FMHY)** upstream project.

### Key Architectural Highlights
- **Multi-Source Failover**: Upstream sources query GitHub Raw, jsDelivr CDN, and GitLab live mirrors sequentially.
- **Fail-Safe Integrity**: If an upstream outage occurs, previous blocklists are strictly retained and never wiped.
- **Pick-and-Choose Categories**: Subscribe only to the specific categories you wish to enforce, or use the unified master list.
- **Fast Synchronization**: Scheduled runs update in near real-time via GitHub Actions.
- **Standard Syntax**: Formatted in standard `||domain^` syntax for AdGuard Home, AdGuard Android/Windows/iOS, Pi-hole, RethinkDNS, and uBlock Origin.

---

## Blocklist Categories & Subscription URLs

| Category | Description | Rules | Raw GitHub Link | Fast CDN Link |
| :--- | :--- | :---: | :--- | :--- |
| **All-in-One (Master)** | Merged & deduplicated master list of all categories | `{all_domains_count:,}` | [`all.txt`]({raw_base}/all.txt) | [`all.txt`]({cdn_base}/all.txt) |
"""
    for cat_key, config in CATEGORIES.items():
        count = category_stats.get(cat_key, 0)
        output_file = config["output"]
        readme_content += f"| **{config['title'].replace('FMHY ', '').replace(' Blocklist', '')}** | {config['description']} | `{count:,}` | [`{output_file}`]({raw_base}/{output_file}) | [`{output_file}`]({cdn_base}/{output_file}) |\n"

    readme_content += f"""
---

## How to Add to Your Adblocker / DNS

### AdGuard Home
1. Navigate to **Filters** -> **DNS blocklists**.
2. Click **Add blocklist** -> **Add a custom list**.
3. Enter a name (e.g. `FMHY Streaming`) and paste the **Raw GitHub Link** or **Fast CDN Link**.
4. Click **Save**.

### uBlock Origin / Brave Shields
1. Open the Extension Settings -> **Filter lists**.
2. Scroll to **Custom** at the bottom.
3. Check the box and paste the link.
4. Click **Apply changes**.

---
*Last automated sync: `{now_str}`*
"""
    with open("README.md", "w", encoding="utf-8") as f:
        f.write(readme_content)
    print("  [+] Generated and updated README.md with live subscription links.")

def main():
    os.makedirs("lists", exist_ok=True)
    session = requests.Session()
    session.headers.update({"User-Agent": "FMHY-Blocklist-Sync-Agent/2.0"})
    
    category_results = {}
    master_domains = set()

    # Parallel processing across categories for high speed
    with ThreadPoolExecutor(max_workers=5) as executor:
        futures = [
            executor.submit(process_category, cat_name, config, session)
            for cat_name, config in CATEGORIES.items()
        ]
        for future in futures:
            cat_name, domains = future.result()
            if domains is not None:
                category_results[cat_name] = len(domains)
                master_domains.update(domains)
            else:
                # If fail-safe retained file, count existing lines
                existing_path = os.path.join("lists", CATEGORIES[cat_name]["output"])
                if os.path.exists(existing_path):
                    with open(existing_path, "r", encoding="utf-8") as ef:
                        lines = [line.strip() for line in ef if line.startswith("||")]
                        category_results[cat_name] = len(lines)
                        master_domains.update(l[2:-1] for l in lines)
                else:
                    category_results[cat_name] = 0

    # Write unified all-in-one blocklist
    all_output_filepath = os.path.join("lists", "all.txt")
    if len(master_domains) >= 10:
        sorted_all = sorted(master_domains)
        with open(all_output_filepath, "w", encoding="utf-8") as f:
            f.write("! Title: FMHY Master All-in-One Blocklist\n")
            f.write("! Description: Complete merged and deduplicated rules from all FMHY categories.\n")
            f.write("! Syntax: AdGuard / Adblock Plus (||domain^)\n")
            f.write("! Generated automatically from FMHY upstream sources\n")
            f.write(f"! Total Rules: {len(sorted_all)}\n")
            f.write(f"! Updated: {datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%d %H:%M:%S UTC')}\n\n")
            for domain in sorted_all:
                f.write(f"||{domain}^\n")
        print(f"\n[MASTER LIST] Wrote {len(sorted_all)} deduplicated rules to {all_output_filepath}")

    # Generate comprehensive README with subscription links
    update_readme(category_results, len(master_domains))

if __name__ == "__main__":
    main()
