import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from collections import Counter
from wordcloud import WordCloud

# -------------------------------
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
plt.show()
