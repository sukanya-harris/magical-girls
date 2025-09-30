import requests
from bs4 import BeautifulSoup
import csv
import time

# -------------------------------
# Archetype keywords
# -------------------------------
archetype_keywords = {
    "Leader/Heart": ["leader", "pink", "love", "hope", "courage"],
    "Cool/Smart": ["blue", "intelligent", "shy", "strategist", "logical"],
    "Healer/Gentle": ["green", "white", "gentle", "healer", "kind", "calm"],
    "Energetic/Trickster": ["yellow", "orange", "energetic", "cheerful", "bubbly", "tomboy"],
    "Mysterious/Dark": ["purple", "black", "mysterious", "tragic", "secretive", "stoic"],
    "Mentor/Guide": ["mentor", "guide", "older", "sister"]
}

# -------------------------------
# Scraper function with keyword tracking
# -------------------------------
def scrape_character(url, series_name):
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")
        
        data = {"Name": None, "Series": series_name, "Color": None, "Powers": None,
                "Notes": None, "Archetype": None, "Matched_Keywords": None}
        title = soup.find("h1")
        if title:
            data["Name"] = title.text.strip()
        
        # Extract infobox text
        infobox = soup.find("table", {"class": "infobox"})
        text_for_keywords = ""
        if infobox:
            for row in infobox.find_all("tr"):
                header = row.find("th")
                cell = row.find("td")
                if header and cell:
                    h = header.text.strip().lower()
                    c = cell.text.strip()
                    text_for_keywords += " " + c.lower()
                    if "color" in h:
                        data["Color"] = c
                        text_for_keywords += " " + c.lower()
                    elif "abilities" in h or "powers" in h:
                        data["Powers"] = c
                    elif "affiliation" in h or "role" in h:
                        data["Notes"] = c
        
        # -------------------------------
        # Smart archetype scoring with keyword tracking
        # -------------------------------
        scores = {arch:0 for arch in archetype_keywords.keys()}
        matched_keywords = {arch: [] for arch in archetype_keywords.keys()}
        
        for arch, keywords in archetype_keywords.items():
            for kw in keywords:
                if kw.lower() in text_for_keywords:
                    scores[arch] += 1
                    matched_keywords[arch].append(kw)
        
        # Assign archetype with highest score
        if max(scores.values()) > 0:
            selected = max(scores, key=scores.get)
            data["Archetype"] = selected
            data["Matched_Keywords"] = ", ".join(matched_keywords[selected])
        else:
            data["Archetype"] = "Unknown"
            data["Matched_Keywords"] = ""
        
        return data
    except Exception as e:
        print(f"Failed to scrape {url}: {e}")
        return None

# -------------------------------
# Series & character list URLs
# -------------------------------
series_list = [
    {"name": "Sailor Moon", "list_url": "https://sailormoon.fandom.com/wiki/Sailor_Guardians#Sailor_Guardians_of_the_Solar_System"},
    {"name": "Pretty Cure", "list_url": "https://prettycure.fandom.com/wiki/Pretty_Cures"},
    {"name": "Winx Club", "list_url": "https://winx.fandom.com/wiki/Winx_(Group)"},
    {"name": "Lolirock", "list_url": "https://lolirock.fandom.com/wiki/Category:Major_Characters"},
    {"name": "Miraculous Ladybug", "list_url": "https://miraculousladybug.fandom.com/wiki/Category:Main_Characters"},
    {"name": "Lilpri", "list_url": "https://lilpri.fandom.com/wiki/Lilpri#Characters"}
    # Add more series here
]

# -------------------------------
# Master scraping loop
# -------------------------------
all_characters = []

for series in series_list:
    print(f"\nScraping series: {series['name']}")
    response = requests.get(series['list_url'])
    soup = BeautifulSoup(response.text, "html.parser")
    
    # Robust container detection
    content = soup.find("div", {"class": "mw-parser-output"}) or soup.find("div", {"id": "mw-content-text"})
    if not content:
        print(f"Could not find content div for {series['name']}")
        continue

    """ # Example: scrape only “Main Characters” section
    content = soup.find("span", {"id": "Main_Characters"})  # heading id
    if content:
        main_section = content.find_parent("h2").find_next_sibling("ul")  # usually a <ul> list
        links = main_section.find_all("a")
    """
    
    links = content.find_all("a")
    character_urls = []
    for link in links:
        href = link.get("href")
        if href and href.startswith("/wiki/") and ":" not in href:
            full_url = "https://" + series['list_url'].split("/")[2] + href
            character_urls.append(full_url)
    
    character_urls = list(set(character_urls))
    print(f"Found {len(character_urls)} characters")
    
    for i, url in enumerate(character_urls):
        print(f"Scraping {i+1}/{len(character_urls)}: {url}")
        char_data = scrape_character(url, series['name'])
        if char_data:
            all_characters.append(char_data)
        time.sleep(1)

# -------------------------------
# Save CSV
# -------------------------------
if all_characters:
    with open("magical_girl_master_dataset_keywords.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=all_characters[0].keys())
        writer.writeheader()
        writer.writerows(all_characters)
    print("\n✅ Saved magical_girl_master_dataset_keywords.csv with matched keywords")
else:
    print("No characters scraped.")
