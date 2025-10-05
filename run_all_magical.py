import pandas as pd
from scraper import scrape_character_page, get_character_urls

# ------------------------------------
# Define the fandoms and section IDs
# ------------------------------------
SERIES_PAGES = {
    "Sailor Moon": {
        "url": "https://sailormoon.fandom.com/wiki/Sailor_Guardians",
        "domain": "https://sailormoon.fandom.com",
        "section_ids": ["Present_(20th_or_21st_Century)"]
    },
    "Winx Club": {
        "url": "https://winx.fandom.com/wiki/Winx_(Group)",
        "domain": "https://winx.fandom.com",
        "section_ids": ["Members"]
    },
    "Pretty Cure": {
        "url": "https://prettycure.fandom.com/wiki/Kimi_to_Idol_Pretty_Cure%E2%99%AA",
        "domain": "https://prettycure.fandom.com",
        "section_ids": ["Pretty_Cure"]
    },
    "Lolirock": {
        "url": "https://lolirock.fandom.com/wiki/LoliRock_(Band)",
        "domain": "https://lolirock.fandom.com",
        "section_ids": ["Members"]
    },
    "Powerpuff Girls": {
        "url": "https://powerpuffgirls.fandom.com/wiki/List_of_characters",
        "domain": "https://powerpuffgirls.fandom.com",
        "section_ids": ["The_Powerpuff_Girls"]
    }
}

# ------------------------------------
# Main scraping routine
# ------------------------------------
def run_all_series():
    all_rows = []

    for series, info in SERIES_PAGES.items():
        print(f"\n🌸 Scraping {series} ...")
        try:
            urls = get_character_urls(info['url'], info['section_ids'], info['domain'])
        except Exception as e:
            print(f"⚠️ Could not retrieve character URLs for {series}: {e}")
            continue

        print(f"   → Found {len(urls)} character links.")
        for i, url in enumerate(urls, start=1):
            print(f"   [{i}/{len(urls)}] Scraping: {url}")
            try:
                data = scrape_character_page(url, series)
                all_rows.append(data)
            except Exception as e:
                print(f"     ❌ Error scraping {url}: {e}")

    # Convert to DataFrame
    df = pd.DataFrame(all_rows)
    print(f"\n✅ Scraping complete! {len(df)} characters collected.")
    df.to_csv("magical_girls_dataset.csv", index=False)
    print("💾 Saved as 'magical_girls_dataset.csv'")
    return df


if __name__ == "__main__":
    df = run_all_series()
    print(df.head())
