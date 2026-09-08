import os
import re
import requests
from urllib.parse import urlparse

# Base endpoints for Primary and Backup mirrors
PRIMARY_BASE = "https://githubusercontent.com"
BACKUP_BASE = "https://gitlab.com"

# Categories mapped to their upstream markdown filenames and generated output file
CATEGORIES = {
    "streaming": {
        "sources": [f"{PRIMARY_BASE}/VideoPiracyGuide.md", f"{BACKUP_BASE}/VideoPiracyGuide.md"],
        "output": "streaming.txt",
        "title": "FMHY Movies & TV Streaming Blocklist"
    },
    "gaming": {
        "sources": [f"{PRIMARY_BASE}/GamingPiracyGuide.md", f"{BACKUP_BASE}/GamingPiracyGuide.md"],
        "output": "gaming.txt",
        "title": "FMHY Gaming Blocklist"
    },
    "audio": {
        "sources": [f"{PRIMARY_BASE}/AudioPiracyGuide.md", f"{BACKUP_BASE}/AudioPiracyGuide.md"],
        "output": "audio.txt",
        "title": "FMHY Music & Audio Blocklist"
    },
    "reading": {
        "sources": [f"{PRIMARY_BASE}/ReadingPiracyGuide.md", f"{BACKUP_BASE}/ReadingPiracyGuide.md"],
        "output": "reading.txt",
        "title": "FMHY Books & Comics Blocklist"
    },
    "downloading": {
        "sources": [f"{PRIMARY_BASE}/DownloadPiracyGuide.md", f"{BACKUP_BASE}/DownloadPiracyGuide.md"],
        "output": "downloading.txt",
        "title": "FMHY Direct Downloads Blocklist"
    },
    "torrenting": {
        "sources": [f"{PRIMARY_BASE}/TorrentPiracyGuide.md", f"{BACKUP_BASE}/TorrentPiracyGuide.md"],
        "output": "torrenting.txt",
        "title": "FMHY Torrents Blocklist"
    },
    "ai": {
        "sources": [f"{PRIMARY_BASE}/AI.md", f"{BACKUP_BASE}/AI.md"],
        "output": "ai.txt",
        "title": "FMHY Artificial Intelligence Blocklist"
    },
    "non-english": {
        "sources": [f"{PRIMARY_BASE}/Non-English.md", f"{BACKUP_BASE}/Non-English.md"],
        "output": "non_english.txt",
        "title": "FMHY International Piracy Blocklist"
    }
}

# Whitelist benign CDNs, tool hosts, and social platforms linked in the wiki
GLOBAL_EXCLUDES = {
    "github.com", "gitlab.com", "reddit.com", "discord.com", "discord.gg",
    "youtube.com", "youtu.be", "google.com", "wikipedia.org", "t.me",
    "archive.org", "twitter.com", "x.com", "patreon.com", "ko-fi.com"
}

def fetch_content_with_failover(sources):
    """Attempts to fetch from primary mirror; cascades to backups on failure."""
    for url in sources:
        try:
            res = requests.get(url, timeout=12)
            if res.status_code == 200 and len(res.text.strip()) > 500:
                print(f"  [+] Ingested successfully from: {url}")
                return res.text
            else:
                print(f"  [!] Mirror HTTP {res.status_code}: {url}")
        except Exception as e:
            print(f"  [!] Connection failed for {url}: {e}")
    return None

def extract_clean_domains(markdown_text):
    """Finds all Markdown links and strips them to unique root domains."""
    # Matches URLs inside standard markdown [Title](https://...)
    raw_urls = re.findall(r'\((https?://[^)\s]+)\)', markdown_text)
    
    domains = set()
    for link in raw_urls:
        try:
            parsed = urlparse(link)
            host = parsed.netloc.lower()
            if host.startswith("www."):
                host = host[4:]
            
            # Filter out port numbers if any
            host = host.split(":")[0]

            if host and "." in host and host not in GLOBAL_EXCLUDES:
                domains.add(host)
        except Exception:
            continue
    return sorted(domains)

def main():
    os.makedirs("lists", exist_ok=True)
    
    for category_name, config in CATEGORIES.items():
        print(f"\nProcessing category: {category_name.upper()}...")
        markdown_data = fetch_content_with_failover(config["sources"])
        
        output_filepath = os.path.join("lists", config["output"])
        
        # FAIL-SAFE GUARD: If all mirrors failed, preserve the old blocklist file
        if not markdown_data:
            print(f"  [CRITICAL] All mirrors failed for {category_name}. Retaining existing file to avoid empty blocklist.")
            continue

        domains = extract_clean_domains(markdown_data)
        
        # Do not overwrite if regex failed to extract meaningful domain counts
        if len(domains) < 10:
            print(f"  [WARNING] Suspiciously low domain count ({len(domains)}). Skipping update to prevent broken list.")
            continue

        # Write out in Adblock / AdGuard Home engine format (||domain^)
        with open(output_filepath, "w", encoding="utf-8") as f:
            f.write(f"! Title: {config['title']}\n")
            f.write("! Generated automatically from FMHY upstream sources\n")
            f.write(f"! Total Rules: {len(domains)}\n\n")
            for domain in domains:
                f.write(f"||{domain}^\n")
                
        print(f"  [SUCCESS] Wrote {len(domains)} rules to {output_filepath}")

if __name__ == "__main__":
    main()
