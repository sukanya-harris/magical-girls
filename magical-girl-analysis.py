import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from collections import Counter
from wordcloud import WordCloud


# Load dataset
df = pd.read_csv("magical_girl_main_characters_dataset.csv")

# Quick look
print("Total characters:", len(df))
print(df.head())

# -----------------------------
# 1. Archetype distribution (all series)
# -----------------------------
archetype_counts = df["Archetype"].value_counts()

plt.figure(figsize=(8,5))
archetype_counts.plot(kind="bar")
plt.title("Archetype Distribution Across All Series")
plt.xlabel("Archetype")
plt.ylabel("Number of Characters")
plt.xticks(rotation=30)
plt.tight_layout()
plt.show()

# -----------------------------
# 2. Archetype distribution by series
# -----------------------------
plt.figure(figsize=(10,6))
pd.crosstab(df["Series"], df["Archetype"]).plot(kind="bar", stacked=True, figsize=(10,6))
plt.title("Archetypes by Series")
plt.xlabel("Series")
plt.ylabel("Count")
plt.legend(title="Archetype")
plt.tight_layout()
plt.show()

# -----------------------------
# 3. Color frequency
# -----------------------------
# Clean up colors (some cells may be NaN)
color_counts = df["Color"].dropna().value_counts()

plt.figure(figsize=(8,5))
color_counts.head(15).plot(kind="bar")
plt.title("Most Common Character Colors")
plt.xlabel("Color")
plt.ylabel("Frequency")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# -----------------------------
# 4. Diversity of archetypes
# -----------------------------
diversity = df.groupby("Series")["Archetype"].nunique()

plt.figure(figsize=(7,5))
diversity.plot(kind="bar", color="purple")
plt.title("Archetype Diversity by Series")
plt.ylabel("Number of Unique Archetypes")
plt.xticks(rotation=30)
plt.tight_layout()
plt.show()

# -----------------------------
# 5. Keyword clouds (optional)
# -----------------------------
# If you want to see what keywords matched most often
from collections import Counter

keywords = []
df["Keywords_Matched"].dropna().apply(lambda x: keywords.extend(x.split(", ")))
keyword_counts = Counter(keywords)

print("\nTop keywords found across all characters:")
print(keyword_counts.most_common(20))

""" # -------------------------------
# Load dataset
# -------------------------------
df = pd.read_csv("magical_girl_master_dataset_keywords.csv")  # your scraped CSV

# -------------------------------
# 1️⃣ Archetype Distribution
# -------------------------------
plt.figure(figsize=(8,5))
df['Archetype'].value_counts().plot(kind='bar', color='pink')
plt.title("Distribution of Magical Girl Archetypes")
plt.ylabel("Number of Characters")
plt.tight_layout()
plt.savefig("archetype_distribution.png")
plt.show()

# -------------------------------
# 2️⃣ Archetype by Series
# -------------------------------
plt.figure(figsize=(10,6))
cross = pd.crosstab(df['Series'], df['Archetype'])
cross.plot(kind='bar', stacked=True, colormap='Pastel1', figsize=(10,6))
plt.title("Archetypes Across Series")
plt.ylabel("Number of Characters")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig("archetype_by_series.png")
plt.show()

# -------------------------------
# 3️⃣ Color-Archetype Heatmap
# -------------------------------
plt.figure(figsize=(10,6))
color_arch = pd.crosstab(df['Color'], df['Archetype'])
sns.heatmap(color_arch, annot=True, fmt="d", cmap="Pastel2")
plt.title("Color vs Archetype Heatmap")
plt.tight_layout()
plt.savefig("color_archetype_heatmap.png")
plt.show()

# -------------------------------
# 4️⃣ Keyword Word Cloud
# -------------------------------
all_keywords = ','.join(df['Matched_Keywords'].dropna())
counter = Counter(all_keywords.split(','))
wordcloud = WordCloud(width=800, height=400, background_color='white').generate_from_frequencies(counter)

plt.figure(figsize=(12,6))
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis('off')
plt.title("Most Common Keywords by Archetype")
plt.tight_layout()
plt.savefig("keywords_wordcloud.png")
plt.show()

# -------------------------------
# 5️⃣ Archetype Diversity per Series
# -------------------------------
plt.figure(figsize=(8,4))
diversity = df.groupby('Series')['Archetype'].nunique()
diversity.plot(kind='barh', color='lavender')
plt.title("Archetype Diversity per Series")
plt.xlabel("Number of Unique Archetypes")
plt.tight_layout()
plt.savefig("archetype_diversity.png")
plt.show() """
