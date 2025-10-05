import re
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from colorthief import ColorThief
from io import BytesIO
import pandas as pd

# ------------------------------
# Helper Functions
# ------------------------------
def extract_dominant_colors(image_url, num_colors=3):
    try:
        response = requests.get(image_url, timeout=10)
        if response.status_code != 200:
            return []
        img_data = BytesIO(response.content)
        color_thief = ColorThief(img_data)
        palette = color_thief.get_palette(color_count=num_colors)
        return [f"rgb{c}" for c in palette]
    except Exception:
        return []
    
def clean_powers(text):
    text = re.sub(r"\([^)]*\d[^)]*\)", "", text)  # remove parentheses with numbers
    text = re.sub(r"\bS\d+\b", "", text)          # remove standalone S6, S7, etc.
    text = re.sub(r"\d{4}", "", text)             # remove years
    text = re.sub(r"\s+", " ", text)              # normalize whitespace
    text = text.strip(" ,;.")
    return text

def extract_archetypes(page_text):

    # Extracts meaningful archetypes from character page text.
    # Filters broad generic terms and uses context-aware keywords.
    text = page_text.lower()

    # Only process if text contains context clues
    context_keywords = ["personality", "archetype", "represents", "known for", "type of girl", "role"]
    if not any(k in text for k in context_keywords):
        return []

    # Refined keyword mapping
    refined_archetypes = {
        "Leader": ["leader", "commander", "captain", "strategist"],
        "Heart": ["optimistic", "kind", "emotional", "hopeful", "cheerful"],
        "Intellectual": ["intelligent", "analytical", "genius", "studious", "logical"],
        "Warrior": ["fighter", "brave", "strong", "combat", "protector"],
        "Artist": ["creative", "artistic", "musician", "performer"],
        "Mystic": ["mysterious", "reserved", "spiritual", "magical affinity"],
        "Rebel": ["tomboy", "independent", "defiant", "free-spirited"],
        "Caregiver": ["healer", "compassionate", "supportive", "empathic"],
    }

    found = []
    for archetype, keywords in refined_archetypes.items():
        if any(k in text for k in keywords):
            found.append(archetype)

    return list(set(found))

# ------------------------------
# Collect character URLs from a section
# ------------------------------
def get_character_urls(base_url, section_ids, domain):
    """
    Finds character links from specified section IDs on a fandom wiki page.
    """
    response = requests.get(base_url, timeout=10)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, "html.parser")

    all_links = set()

    for section_id in section_ids:
        header = soup.find(id=section_id)
        if not header:
            print(f"⚠️ Section '{section_id}' not found on {base_url}")
            continue

        # Collect all <a> tags until next section
        for sibling in header.find_all_next(["a", "h2", "h3", "div"], limit=200):
            if sibling.name in ["h2", "h3"]:
                break
            if sibling.name == "a" and sibling.get("href"):
                href = sibling["href"]
                if href.startswith("/wiki/") and not any(x in href for x in ["Category:", "Episode:", "List_of", "Help:"]):
                    full_url = urljoin(domain, href)
                    all_links.add(full_url)

    return list(all_links)

# ------------------------------
# Step 2: Scrape character page
# ------------------------------
def scrape_character_page(url, series_name):
    response = requests.get(url, timeout=10)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, "html.parser")

    # Character name
    name_tag = soup.find("h1", class_="page-header__title")
    name = name_tag.text.strip() if name_tag else url.split("/")[-1].replace("_", " ")

    # Powers
    powers = []
    power_labels = ["Power", "Powers", "Abilities", "Skills", "Attacks", "Techniques", "Weapon"]
    for label in power_labels:
        found = soup.find("h3", string=re.compile(label, re.IGNORECASE))
        if found:
            section_text = []
            for sibling in found.find_all_next(["p", "li"], limit=5):
                if sibling.name in ["h2", "h3"]:
                    break
                section_text.append(sibling.get_text(" ", strip=True))
            powers.append(" ".join(section_text))
    powers = clean_powers(", ".join(powers))

    # Full page text for archetype extraction
    page_text = soup.get_text(separator=" ", strip=True)
    archetypes = extract_archetypes(page_text)

    # Image for dominant color
    image = (
        soup.select_one(".pi-image-thumbnail") or
        soup.select_one("image-thumbnail") or
        soup.select_one(".image") or
        soup.find("img")
    )
    image_url = None
    if image:
        image_url = image.get("src") or image.get("data-src")
        
    # Image URL
    img_url = ""
    img_div = soup.find("div", class_=re.compile("pi-image|pi-media"))
    if img_div:
        img_tag = img_div.find("img")
        if img_tag:
            img_url = img_tag.get("data-src") or img_tag.get("src") or ""


    dominant_colors = extract_dominant_colors(image_url) if image_url else []

    return {
        "Name": name,
        "Series": series_name,
        "Wiki URL": url,
        "Powers": powers if powers else None,
        "Archetypes": ", ".join(archetypes) if archetypes else None,
        "Dominant Colors": ", ".join(dominant_colors) if dominant_colors else None,
        "Image URL": img_url
    }
