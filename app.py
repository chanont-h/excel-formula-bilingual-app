
import streamlit as st
import json
import pyperclip
from fuzzywuzzy import fuzz
import base64

# ===== Load Language =====
def load_lang():
    with open("lang/lang_en.json", "r", encoding="utf-8") as f:
        return json.load(f)

# ===== Load Data =====
@st.cache_data
def load_data():
    with open("functions_en_th_completed.json", "r", encoding="utf-8") as f:
        return json.load(f)

functions = load_data()
lang = load_lang()

if "favorites" not in st.session_state:
    st.session_state.favorites = []

st.title("🔍 Excel Formula Helper (v1.2.0)")

# ===== Filter Sidebar =====
st.sidebar.header("🔎 Advanced Filter")
category_filter = st.sidebar.multiselect("📂 Category", list(set(f["Category"] for f in functions)))
difficulty_filter = st.sidebar.multiselect("⚙️ Difficulty", list(set(f.get("difficulty", "") for f in functions)))

st.sidebar.markdown("⭐️ **My Favorites**")
for fav in st.session_state.favorites:
    st.sidebar.write(f"- {fav}")

# ===== Search =====
query = st.text_input(lang["search_placeholder"], "")

# ===== Filter + Search =====
def filter_function(f):
    match_query = query.lower() in f["syntax_en"].lower() if query else True
    match_cat = f["Category"] in category_filter if category_filter else True
    match_diff = f.get("difficulty", "") in difficulty_filter if difficulty_filter else True
    return match_query and match_cat and match_diff

results = [f for f in functions if filter_function(f)]

# ===== Show Results =====
if results:
    for f in results:
        with st.container():
            st.subheader(f["syntax_en"])
            st.code(f["example_en"], language="plaintext")

            st.markdown(f"📂 **Category:** {f.get('Category', '')}")

            col1, col2, col3 = st.columns(3)
            with col1:
                if st.button(f"📋 Copy {f['syntax_en']}", key=f"copy_{f['syntax_en']}"):
                    pyperclip.copy(f["example_en"])
                    st.success("Copied to clipboard!")
            with col2:
                if st.button(f"⭐️ Bookmark", key=f"fav_{f['syntax_en']}"):
                    if f["syntax_en"] not in st.session_state.favorites:
                        st.session_state.favorites.append(f["syntax_en"])
                        st.success(f"Added {f['syntax_en']} to favorites!")
            with col3:
                if st.button("📄 Export Tutorial", key=f"md_{f['syntax_en']}"):
                    content = f"# {f['syntax_en']}\n\n"
                    content += f"**Example:** `{f['example_en']}`\n\n"
                    for i in range(1, 5):
                        step = f"Tutorial_{i}"
                        if f.get(step):
                            content += f"**Step {i}:** {f[step]}\n\n"
                    b64 = base64.b64encode(content.encode()).decode()
                    href = f'<a href="data:text/markdown;base64,{b64}" download="{f["syntax_en"]}_tutorial.md">📥 Download Markdown</a>'
                    st.markdown(href, unsafe_allow_html=True)

            with st.expander("📖 Tutorial"):
                for i in range(1, 5):
                    step = f"Tutorial_{i}"
                    if f.get(step):
                        st.markdown(f"**Step {i}:** {f[step]}")
else:
    if query or category_filter or difficulty_filter:
        st.warning(lang["not_found"])
