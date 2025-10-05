import streamlit as st
import pandas as pd
import re
import plotly.express as px

# === Load dataset ===
df = pd.read_csv("magical_girls_dataset.csv")
df["Image URL"] = df["Image URL"].astype(str)
df["Image URL"] = df["Image URL"].str.strip().str.replace('"', '')
df.fillna("", inplace=True)

# === Helper Functions ===
def parse_rgb_string(rgb_str):
    """Convert string like 'rgb(213, 194, 175), rgb(72, 90, 137)' into list of tuples."""
    if not rgb_str or pd.isna(rgb_str):
        return []
    rgb_str = str(rgb_str)
    matches = re.findall(r"rgb\((\d+),\s*(\d+),\s*(\d+)\)", rgb_str)
    return [tuple(map(int, m)) for m in matches]

def rgb_to_hex(rgb_tuple):
    """Convert RGB tuple to hex string for CSS"""
    return '#%02x%02x%02x' % rgb_tuple

# === Sidebar Filters ===
st.sidebar.header("Filters")
series_options = df["Series"].dropna().unique().tolist()
selected_series = st.sidebar.multiselect("Select Series", series_options, default=series_options)
filtered_df = df[df["Series"].isin(selected_series)]

# Archetype filter
all_archetypes = set()
for arch in filtered_df["Archetypes"]:
    if pd.notna(arch) and arch != "":
        all_archetypes.update([a.strip() for a in str(arch).split(",") if a.strip()])
all_archetypes = sorted(list(all_archetypes))

selected_archetypes = st.sidebar.multiselect("Select Archetypes", all_archetypes, default=all_archetypes)

if selected_archetypes:
    def has_selected_archetype(arch_str):
        chars = [a.strip() for a in str(arch_str).split(",") if a.strip()]
        return any(a in chars for a in selected_archetypes)
    filtered_df = filtered_df[filtered_df["Archetypes"].apply(has_selected_archetype)]

# Name search
search_name = st.sidebar.text_input("Search Character")

# Apply filters
def filter_row(row):
    # Series
    if row["Series"] not in selected_series:
        return False
    # Archetypes
    arch_value = row.get("Archetypes", "")
    if arch_value and pd.notna(arch_value):
        arch_list = [a.strip() for a in str(arch_value).split(",") if a.strip()]
        if not any(a in selected_archetypes for a in arch_list):
            return False
    else:
        return False  # No archetypes
    # Name
    if search_name and search_name.lower() not in str(row["Name"]).lower():
        return False
    return True

filtered_df = df[df.apply(filter_row, axis=1)]

# === Main App ===

# === Page Title ===
st.title("🌸 Magical Girl Dashboard")
st.markdown("Explore characters, archetypes, and dominant colors across multiple series.")


# === Character Overview ===
st.header("🧙‍♀️ Character Overview")

for _, row in filtered_df.iterrows():
    cols = st.columns([1, 2])
    
    # Image
    img_url = row.get("Image URL", "")
    if img_url and img_url.strip().startswith("http"):
        try:
            cols[0].image(img_url, width=300)
        except:
            cols[0].text("No image")
    else:
        cols[0].text("No image")

    # Name + Series
    cols[1].markdown(f"**{row['Name']}**")
    cols[1].markdown(f"*{row['Series']}*")

    # Archetypes
    arch_value = row.get("Archetypes", "")
    if arch_value and pd.notna(arch_value):
        archetypes_list = [a.strip() for a in str(arch_value).split(",") if a.strip()]
        archetypes_list = archetypes_list[:3]
        cols[1].markdown(", ".join(archetypes_list))
    else:
        cols[1].markdown("No archetypes")

    # Dominant Colors
    colors_value = row.get("Dominant Colors", "")
    colors = parse_rgb_string(colors_value)
    if colors:
        max_cols = min(len(colors), 5)
        color_cols = cols[1].columns(max_cols)
        for c_col, c_rgb in zip(color_cols, colors[:max_cols]):
            hex_color = rgb_to_hex(c_rgb)
            rgb_text = f"RGB{c_rgb}"
            c_col.markdown(
                f"<div style='background-color:{hex_color};width:100%;height:40px;border-radius:6px;'></div>",
                unsafe_allow_html=True
            )
    else:
        cols[1].markdown("No colors")

    st.markdown("<hr>", unsafe_allow_html=True)

# ------------------------------
# Radar Chart: Archetype Distribution by Series
# ------------------------------
st.header("📊 Archetype Distribution by Series")

archetype_cols = ["Leader", "Heart", "Intellectual", "Warrior", "Artist", "Mystic", "Rebel", "Caregiver"]

# One-hot encode archetypes
for arch in archetype_cols:
    filtered_df[arch] = filtered_df["Archetypes"].apply(lambda x: 1 if x and arch in str(x) else 0)

# Aggregate counts by series
df_series = filtered_df.groupby("Series")[archetype_cols].sum().reset_index()

# Melt to long-form for Plotly
df_melted = df_series.melt(id_vars="Series", value_vars=archetype_cols, var_name="Archetype", value_name="Count")

# Assign distinct colors per series
series_colors = {
    "Sailor Moon": "#F06292",
    "Winx Club": "#42A5F5",
    "Pretty Cure": "#FFB74D"
}

# Radar chart
fig = px.line_polar(
    df_melted,
    r="Count",
    theta="Archetype",
    color="Series",
    line_close=True,
    color_discrete_map=series_colors
)

fig.update_traces(fill='toself')
fig.update_layout(
    title="Archetype Distribution by Series",
    polar=dict(radialaxis=dict(visible=True, tickfont=dict(size=10)))
)

st.plotly_chart(fig, use_container_width=True)

st.caption("✨ Data collected and analyzed using custom scraper.")
