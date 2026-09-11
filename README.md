# FMHY Multi-Category Blocklists

Automated, high-frequency AdGuard / DNS / uBlock / personalDNSfilter blocklists synchronized directly from the **FreeMediaHeckYeah (FMHY)** upstream project.

### Key Architectural Highlights
- **Dual Syntax Available**:
  - **Hosts / Plain Domain (`domain`)**: For **personalDNSfilter (pDNSf)**, Pi-hole, and local DNS resolvers.
  - **AdGuard / Adblock Plus (`||domain^`)**: For AdGuard Home, AdGuard apps, and uBlock Origin.
- **Multi-Source Failover**: Upstream sources query GitHub Raw, jsDelivr CDN, and GitLab live mirrors sequentially.
- **Fail-Safe Integrity**: If an upstream outage occurs, previous blocklists are strictly retained and never wiped.
- **Pick-and-Choose Categories**: Subscribe only to the specific categories you wish to enforce, or use the unified master list.
- **Fast Synchronization**: Scheduled runs update in near real-time via GitHub Actions.

---

## Blocklist Categories & Subscription URLs

### 1. Hosts / Plain Domain Format (For personalDNSfilter & Pi-hole)

| Category | Rules | Raw GitHub Link (personalDNSfilter) | Fast CDN Link |
| :--- | :---: | :--- | :--- |
| **All-in-One (Master)** | `6,102` | [`lists/hosts/all.txt`](https://raw.githubusercontent.com/pratham-1002-adg/fmhy-blocklists/main/lists/hosts/all.txt) | [`hosts/all.txt`](https://cdn.jsdelivr.net/gh/pratham-1002-adg/fmhy-blocklists@main/lists/hosts/all.txt) |
| **Movies & TV Streaming** | `1,089` | [`streaming.txt`](https://raw.githubusercontent.com/pratham-1002-adg/fmhy-blocklists/main/lists/hosts/streaming.txt) | [`streaming.txt`](https://cdn.jsdelivr.net/gh/pratham-1002-adg/fmhy-blocklists@main/lists/hosts/streaming.txt) |
| **Gaming** | `1,029` | [`gaming.txt`](https://raw.githubusercontent.com/pratham-1002-adg/fmhy-blocklists/main/lists/hosts/gaming.txt) | [`gaming.txt`](https://cdn.jsdelivr.net/gh/pratham-1002-adg/fmhy-blocklists@main/lists/hosts/gaming.txt) |
| **Music & Audio** | `880` | [`audio.txt`](https://raw.githubusercontent.com/pratham-1002-adg/fmhy-blocklists/main/lists/hosts/audio.txt) | [`audio.txt`](https://cdn.jsdelivr.net/gh/pratham-1002-adg/fmhy-blocklists@main/lists/hosts/audio.txt) |
| **Books & Comics** | `854` | [`reading.txt`](https://raw.githubusercontent.com/pratham-1002-adg/fmhy-blocklists/main/lists/hosts/reading.txt) | [`reading.txt`](https://cdn.jsdelivr.net/gh/pratham-1002-adg/fmhy-blocklists@main/lists/hosts/reading.txt) |
| **Direct Downloads** | `149` | [`downloading.txt`](https://raw.githubusercontent.com/pratham-1002-adg/fmhy-blocklists/main/lists/hosts/downloading.txt) | [`downloading.txt`](https://cdn.jsdelivr.net/gh/pratham-1002-adg/fmhy-blocklists@main/lists/hosts/downloading.txt) |
| **Torrents** | `99` | [`torrenting.txt`](https://raw.githubusercontent.com/pratham-1002-adg/fmhy-blocklists/main/lists/hosts/torrenting.txt) | [`torrenting.txt`](https://cdn.jsdelivr.net/gh/pratham-1002-adg/fmhy-blocklists@main/lists/hosts/torrenting.txt) |
| **Mobile Piracy** | `484` | [`mobile.txt`](https://raw.githubusercontent.com/pratham-1002-adg/fmhy-blocklists/main/lists/hosts/mobile.txt) | [`mobile.txt`](https://cdn.jsdelivr.net/gh/pratham-1002-adg/fmhy-blocklists@main/lists/hosts/mobile.txt) |
| **Artificial Intelligence** | `272` | [`ai.txt`](https://raw.githubusercontent.com/pratham-1002-adg/fmhy-blocklists/main/lists/hosts/ai.txt) | [`ai.txt`](https://cdn.jsdelivr.net/gh/pratham-1002-adg/fmhy-blocklists@main/lists/hosts/ai.txt) |
| **International Piracy** | `1,489` | [`non_english.txt`](https://raw.githubusercontent.com/pratham-1002-adg/fmhy-blocklists/main/lists/hosts/non_english.txt) | [`non_english.txt`](https://cdn.jsdelivr.net/gh/pratham-1002-adg/fmhy-blocklists@main/lists/hosts/non_english.txt) |

### 2. AdGuard / Adblock Syntax Format (`||domain^`)

| Category | Rules | Raw GitHub Link (AdGuard Home / uBlock) | Fast CDN Link |
| :--- | :---: | :--- | :--- |
| **All-in-One (Master)** | `6,102` | [`lists/all.txt`](https://raw.githubusercontent.com/pratham-1002-adg/fmhy-blocklists/main/lists/all.txt) | [`all.txt`](https://cdn.jsdelivr.net/gh/pratham-1002-adg/fmhy-blocklists@main/lists/all.txt) |
| **Movies & TV Streaming** | `1,089` | [`streaming.txt`](https://raw.githubusercontent.com/pratham-1002-adg/fmhy-blocklists/main/lists/streaming.txt) | [`streaming.txt`](https://cdn.jsdelivr.net/gh/pratham-1002-adg/fmhy-blocklists@main/lists/streaming.txt) |
| **Gaming** | `1,029` | [`gaming.txt`](https://raw.githubusercontent.com/pratham-1002-adg/fmhy-blocklists/main/lists/gaming.txt) | [`gaming.txt`](https://cdn.jsdelivr.net/gh/pratham-1002-adg/fmhy-blocklists@main/lists/gaming.txt) |
| **Music & Audio** | `880` | [`audio.txt`](https://raw.githubusercontent.com/pratham-1002-adg/fmhy-blocklists/main/lists/audio.txt) | [`audio.txt`](https://cdn.jsdelivr.net/gh/pratham-1002-adg/fmhy-blocklists@main/lists/audio.txt) |
| **Books & Comics** | `854` | [`reading.txt`](https://raw.githubusercontent.com/pratham-1002-adg/fmhy-blocklists/main/lists/reading.txt) | [`reading.txt`](https://cdn.jsdelivr.net/gh/pratham-1002-adg/fmhy-blocklists@main/lists/reading.txt) |
| **Direct Downloads** | `149` | [`downloading.txt`](https://raw.githubusercontent.com/pratham-1002-adg/fmhy-blocklists/main/lists/downloading.txt) | [`downloading.txt`](https://cdn.jsdelivr.net/gh/pratham-1002-adg/fmhy-blocklists@main/lists/downloading.txt) |
| **Torrents** | `99` | [`torrenting.txt`](https://raw.githubusercontent.com/pratham-1002-adg/fmhy-blocklists/main/lists/torrenting.txt) | [`torrenting.txt`](https://cdn.jsdelivr.net/gh/pratham-1002-adg/fmhy-blocklists@main/lists/torrenting.txt) |
| **Mobile Piracy** | `484` | [`mobile.txt`](https://raw.githubusercontent.com/pratham-1002-adg/fmhy-blocklists/main/lists/mobile.txt) | [`mobile.txt`](https://cdn.jsdelivr.net/gh/pratham-1002-adg/fmhy-blocklists@main/lists/mobile.txt) |
| **Artificial Intelligence** | `272` | [`ai.txt`](https://raw.githubusercontent.com/pratham-1002-adg/fmhy-blocklists/main/lists/ai.txt) | [`ai.txt`](https://cdn.jsdelivr.net/gh/pratham-1002-adg/fmhy-blocklists@main/lists/ai.txt) |
| **International Piracy** | `1,489` | [`non_english.txt`](https://raw.githubusercontent.com/pratham-1002-adg/fmhy-blocklists/main/lists/non_english.txt) | [`non_english.txt`](https://cdn.jsdelivr.net/gh/pratham-1002-adg/fmhy-blocklists@main/lists/non_english.txt) |

---

## How to Add to Your Tool

### personalDNSfilter (pDNSf) on Android
1. Open personalDNSfilter -> **Advanced settings** -> **Configure filter update**.
2. Tap the edit pencil on `<new>` (or existing slot).
3. Name: `FMHY Master (Hosts)`
4. URL: `https://raw.githubusercontent.com/pratham-1002-adg/fmhy-blocklists/main/lists/hosts/all.txt` (or `https://raw.githubusercontent.com/pratham-1002-adg/fmhy-blocklists/main/lists/hosts/streaming.txt`)
5. Check the box `☑` to activate.
6. Return to main screen and tap **`RELOAD FILTER`**.

### AdGuard Home
1. Navigate to **Filters** -> **DNS blocklists**.
2. Click **Add blocklist** -> **Add a custom list**.
3. Name: `FMHY Master`
4. URL: `https://raw.githubusercontent.com/pratham-1002-adg/fmhy-blocklists/main/lists/all.txt`
5. Click **Save**.

---
*Last automated sync: `2026-09-11 07:08:04 UTC`*
