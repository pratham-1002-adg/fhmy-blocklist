# FMHY Multi-Category Blocklists

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
| **All-in-One (Master)** | Merged & deduplicated master list of all categories | `5,966` | [`all.txt`](https://raw.githubusercontent.com/pratham-1002-adg/fmhy-blocklists/main/lists/all.txt) | [`all.txt`](https://cdn.jsdelivr.net/gh/pratham-1002-adg/fmhy-blocklists@main/lists/all.txt) |
| **Movies & TV Streaming** | Movies, TV shows, anime, cartoon, sports streaming, and video aggregators. | `1,058` | [`streaming.txt`](https://raw.githubusercontent.com/pratham-1002-adg/fmhy-blocklists/main/lists/streaming.txt) | [`streaming.txt`](https://cdn.jsdelivr.net/gh/pratham-1002-adg/fmhy-blocklists@main/lists/streaming.txt) |
| **Gaming** | Pirated games, ROMs, ISOs, game repacks, cracks, and emulators. | `1,017` | [`gaming.txt`](https://raw.githubusercontent.com/pratham-1002-adg/fmhy-blocklists/main/lists/gaming.txt) | [`gaming.txt`](https://cdn.jsdelivr.net/gh/pratham-1002-adg/fmhy-blocklists@main/lists/gaming.txt) |
| **Music & Audio** | Music streaming, lossless downloads, rippers, podcasts, and audiobooks. | `867` | [`audio.txt`](https://raw.githubusercontent.com/pratham-1002-adg/fmhy-blocklists/main/lists/audio.txt) | [`audio.txt`](https://cdn.jsdelivr.net/gh/pratham-1002-adg/fmhy-blocklists@main/lists/audio.txt) |
| **Books & Comics** | E-books, textbooks, comics, manga, light novels, and magazines. | `841` | [`reading.txt`](https://raw.githubusercontent.com/pratham-1002-adg/fmhy-blocklists/main/lists/reading.txt) | [`reading.txt`](https://cdn.jsdelivr.net/gh/pratham-1002-adg/fmhy-blocklists@main/lists/reading.txt) |
| **Direct Downloads** | Direct download (DDL) portals, file lockers, premium debrid services. | `149` | [`downloading.txt`](https://raw.githubusercontent.com/pratham-1002-adg/fmhy-blocklists/main/lists/downloading.txt) | [`downloading.txt`](https://cdn.jsdelivr.net/gh/pratham-1002-adg/fmhy-blocklists@main/lists/downloading.txt) |
| **Torrents** | Public & private torrent trackers, indexers, and P2P search engines. | `97` | [`torrenting.txt`](https://raw.githubusercontent.com/pratham-1002-adg/fmhy-blocklists/main/lists/torrenting.txt) | [`torrenting.txt`](https://cdn.jsdelivr.net/gh/pratham-1002-adg/fmhy-blocklists@main/lists/torrenting.txt) |
| **Mobile Piracy** | Modded Android APKs, sideloading stores, iOS IPA repositories. | `479` | [`mobile.txt`](https://raw.githubusercontent.com/pratham-1002-adg/fmhy-blocklists/main/lists/mobile.txt) | [`mobile.txt`](https://cdn.jsdelivr.net/gh/pratham-1002-adg/fmhy-blocklists@main/lists/mobile.txt) |
| **Artificial Intelligence** | AI scrapers, unsanctioned bot mirrors, model rippers, and jailbreaks. | `263` | [`ai.txt`](https://raw.githubusercontent.com/pratham-1002-adg/fmhy-blocklists/main/lists/ai.txt) | [`ai.txt`](https://cdn.jsdelivr.net/gh/pratham-1002-adg/fmhy-blocklists@main/lists/ai.txt) |
| **International Piracy** | Non-English and regional piracy, streaming, and media portals. | `1,431` | [`non_english.txt`](https://raw.githubusercontent.com/pratham-1002-adg/fmhy-blocklists/main/lists/non_english.txt) | [`non_english.txt`](https://cdn.jsdelivr.net/gh/pratham-1002-adg/fmhy-blocklists@main/lists/non_english.txt) |

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
*Last automated sync: `2026-09-08 02:28:49 UTC`*
