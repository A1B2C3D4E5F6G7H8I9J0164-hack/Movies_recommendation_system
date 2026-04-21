import requests
import streamlit as st

# =============================
# CONFIG
# =============================
API_BASE = "http://127.0.0.1:8000"
TMDB_IMG = "https://image.tmdb.org/t/p/w500"

st.set_page_config(page_title="Cinerama", page_icon="🎞️", layout="wide")

# ─────────────────────────────────────────────────────────────────────────────
# GLOBAL CSS — Luxury Cinema / Editorial
# ─────────────────────────────────────────────────────────────────────────────
st.markdown("""
<link href="https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,400;0,600;0,700;1,400;1,600&family=DM+Sans:wght@300;400;500;600&family=DM+Mono:wght@400&display=swap" rel="stylesheet">

<style>
/* ══════════════════════════════
   CSS VARIABLES & RESET
══════════════════════════════ */
:root {
  --bg-base:       #080605;
  --bg-surface:    #110e0c;
  --bg-elevated:   #1a1512;
  --bg-hover:      #221c17;
  --border-subtle: rgba(245,200,100,0.08);
  --border-mid:    rgba(245,200,100,0.16);
  --border-glow:   rgba(245,200,100,0.35);
  --gold:          #f0c060;
  --gold-dim:      #c89840;
  --gold-bright:   #fad97a;
  --text-primary:  #f5ede0;
  --text-secondary:#a89070;
  --text-muted:    #6a5545;
  --accent-red:    #d45050;
  --font-display:  'Playfair Display', Georgia, serif;
  --font-body:     'DM Sans', sans-serif;
  --font-mono:     'DM Mono', monospace;
  --radius-sm:     8px;
  --radius-md:     12px;
  --radius-lg:     20px;
  --shadow-card:   0 4px 24px rgba(0,0,0,0.7), 0 1px 4px rgba(0,0,0,0.5);
  --shadow-hover:  0 12px 48px rgba(0,0,0,0.85), 0 0 0 1px var(--border-glow), 0 0 32px rgba(240,192,96,0.12);
  --transition:    0.25s cubic-bezier(0.4,0,0.2,1);
}

/* ══════════════════════════════
   GLOBAL BACKGROUND + GRAIN
══════════════════════════════ */
html, body,
[data-testid="stAppViewContainer"],
[data-testid="stAppViewContainer"] > .main {
  background-color: var(--bg-base) !important;
  color: var(--text-primary) !important;
  font-family: var(--font-body) !important;
}

/* Film grain overlay */
[data-testid="stAppViewContainer"]::before {
  content: '';
  position: fixed;
  inset: 0;
  pointer-events: none;
  z-index: 9999;
  opacity: 0.028;
  background-image: url("data:image/svg+xml,%3Csvg viewBox='0 0 512 512' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='noise'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.75' numOctaves='4' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23noise)'/%3E%3C/svg%3E");
  background-size: 200px 200px;
}

/* Warm vignette on main content */
.main .block-container {
  background: radial-gradient(ellipse 90% 70% at 50% 0%, rgba(240,192,96,0.03) 0%, transparent 60%) !important;
  max-width: 1400px !important;
  padding: 2rem 2.5rem 4rem !important;
}

/* ══════════════════════════════
   HEADER / APP BAR
══════════════════════════════ */
[data-testid="stHeader"] {
  background: rgba(8,6,5,0.92) !important;
  backdrop-filter: blur(12px) !important;
  border-bottom: 1px solid var(--border-subtle) !important;
}

/* ══════════════════════════════
   TYPOGRAPHY
══════════════════════════════ */
h1, h2, h3, h4 {
  font-family: var(--font-display) !important;
  color: var(--text-primary) !important;
  letter-spacing: -0.02em !important;
}
h1 { font-size: 2.8rem !important; font-weight: 700 !important; }
h2 { font-size: 1.9rem !important; font-weight: 600 !important; }
h3 { font-size: 1.35rem !important; font-weight: 600 !important; }

p, label {
  font-family: var(--font-body);
}

/* ══════════════════════════════
   SIDEBAR
══════════════════════════════ */
[data-testid="stSidebar"] {
  background: #0c0a08 !important;
  border-right: 1px solid var(--border-subtle) !important;
  padding: 0 !important;
}
[data-testid="stSidebar"] > div {
  padding: 2rem 1.5rem !important;
}

/* Sidebar headings */
[data-testid="stSidebar"] h2,
[data-testid="stSidebar"] h3 {
  font-family: var(--font-display) !important;
  color: var(--gold) !important;
  font-size: 1.2rem !important;
  letter-spacing: 0.04em !important;
}

/* Sidebar label text */
[data-testid="stSidebar"] label,
[data-testid="stSidebar"] .stSelectbox label,
[data-testid="stSidebar"] .stSlider label {
  color: var(--text-secondary) !important;
  font-size: 0.78rem !important;
  text-transform: uppercase !important;
  letter-spacing: 0.1em !important;
  font-weight: 600 !important;
}

/* ══════════════════════════════
   INPUTS
══════════════════════════════ */
.stTextInput > div > div > input {
  background: var(--bg-surface) !important;
  border: 1px solid var(--border-mid) !important;
  border-radius: var(--radius-md) !important;
  color: var(--text-primary) !important;
  font-family: var(--font-body) !important;
  font-size: 1rem !important;
  padding: 0.75rem 1.1rem !important;
  transition: border-color var(--transition), box-shadow var(--transition) !important;
  caret-color: var(--gold) !important;
}
.stTextInput > div > div > input::placeholder {
  color: var(--text-muted) !important;
}
.stTextInput > div > div > input:focus {
  border-color: var(--gold-dim) !important;
  box-shadow: 0 0 0 3px rgba(240,192,96,0.1), 0 0 16px rgba(240,192,96,0.06) !important;
  outline: none !important;
}
.stTextInput label {
  color: var(--text-secondary) !important;
  font-size: 0.78rem !important;
  text-transform: uppercase !important;
  letter-spacing: 0.1em !important;
  font-weight: 600 !important;
}

/* Selectbox */
.stSelectbox > div > div {
  background: var(--bg-surface) !important;
  border: 1px solid var(--border-mid) !important;
  border-radius: var(--radius-md) !important;
  color: var(--text-primary) !important;
  transition: border-color var(--transition) !important;
}
.stSelectbox > div > div:hover {
  border-color: var(--gold-dim) !important;
}
.stSelectbox > div > div > div {
  color: var(--text-primary) !important;
  font-family: var(--font-body) !important;
}

/* Slider */
.stSlider > div {
  color: var(--text-secondary) !important;
}
[data-baseweb="slider"] [role="slider"] {
  background: var(--gold) !important;
  border-color: var(--gold) !important;
  box-shadow: 0 0 0 3px rgba(240,192,96,0.25) !important;
}
[data-baseweb="slider"] div[data-testid="stSliderTrackActive"] {
  background: linear-gradient(90deg, var(--gold-dim), var(--gold)) !important;
}

/* ══════════════════════════════
   BUTTONS
══════════════════════════════ */
.stButton > button {
  background: transparent !important;
  color: var(--text-secondary) !important;
  border: 1px solid var(--border-mid) !important;
  border-radius: var(--radius-sm) !important;
  font-family: var(--font-body) !important;
  font-size: 0.8rem !important;
  font-weight: 500 !important;
  letter-spacing: 0.06em !important;
  text-transform: uppercase !important;
  padding: 0.4rem 1rem !important;
  transition: all var(--transition) !important;
  width: 100% !important;
}
.stButton > button:hover {
  background: var(--gold) !important;
  color: var(--bg-base) !important;
  border-color: var(--gold) !important;
  box-shadow: 0 0 16px rgba(240,192,96,0.3) !important;
  transform: translateY(-1px) !important;
}
.stButton > button:active {
  transform: translateY(0) !important;
}

/* ══════════════════════════════
   DIVIDER / HR
══════════════════════════════ */
hr, [data-testid="stDivider"] {
  border: none !important;
  border-top: 1px solid var(--border-subtle) !important;
  margin: 2rem 0 !important;
}

/* ══════════════════════════════
   MOVIE CARD
══════════════════════════════ */
.cine-card {
  background: var(--bg-surface);
  border: 1px solid var(--border-subtle);
  border-radius: var(--radius-md);
  overflow: hidden;
  position: relative;
  height: 100%;
  transition: transform var(--transition), box-shadow var(--transition), border-color var(--transition);
  box-shadow: var(--shadow-card);
}
.cine-card:hover {
  transform: translateY(-6px) scale(1.015);
  box-shadow: var(--shadow-hover);
  border-color: var(--border-glow);
}
.cine-card::after {
  content: '';
  position: absolute;
  inset: 0;
  border-radius: var(--radius-md);
  background: linear-gradient(180deg, transparent 55%, rgba(8,6,5,0.95) 100%);
  pointer-events: none;
}

/* Poster image wrapper */
.cine-poster-wrap {
  position: relative;
  width: 100%;
  aspect-ratio: 2/3;
  background: var(--bg-elevated);
  overflow: hidden;
}
.cine-poster-wrap img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  display: block;
  transition: transform 0.5s ease;
}
.cine-card:hover .cine-poster-wrap img {
  transform: scale(1.05);
}

/* No poster placeholder */
.cine-no-poster {
  width: 100%;
  aspect-ratio: 2/3;
  background: linear-gradient(135deg, var(--bg-elevated) 0%, #1f1710 100%);
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
  color: var(--text-muted);
  font-size: 2rem;
}
.cine-no-poster span {
  font-size: 0.75rem;
  font-family: var(--font-mono);
  text-transform: uppercase;
  letter-spacing: 0.12em;
}

/* Card title overlay */
.cine-card-body {
  padding: 0.85rem 0.9rem 0.5rem;
}
.cine-card-title {
  font-family: var(--font-display);
  font-size: 0.88rem;
  font-weight: 600;
  color: var(--text-primary);
  line-height: 1.35;
  height: 2.4rem;
  overflow: hidden;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  margin-bottom: 0.6rem;
  letter-spacing: -0.01em;
}

/* ══════════════════════════════
   SECTION LABELS
══════════════════════════════ */
.section-label {
  display: inline-flex;
  align-items: center;
  gap: 0.6rem;
  font-family: var(--font-body);
  font-size: 0.7rem;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.14em;
  color: var(--gold);
  margin-bottom: 1.5rem;
  padding-bottom: 0.6rem;
  border-bottom: 1px solid var(--border-mid);
  width: 100%;
}
.section-label::before {
  content: '';
  display: inline-block;
  width: 18px;
  height: 2px;
  background: linear-gradient(90deg, var(--gold), transparent);
  flex-shrink: 0;
}

/* ══════════════════════════════
   HERO TITLE
══════════════════════════════ */
.hero-wrap {
  padding: 1.5rem 0 2rem;
  position: relative;
}
.hero-eyebrow {
  font-family: var(--font-mono);
  font-size: 0.7rem;
  color: var(--gold-dim);
  text-transform: uppercase;
  letter-spacing: 0.2em;
  margin-bottom: 0.5rem;
}
.hero-title {
  font-family: var(--font-display) !important;
  font-size: 3.2rem !important;
  font-weight: 700 !important;
  line-height: 1.05 !important;
  background: linear-gradient(135deg, var(--text-primary) 30%, var(--gold) 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  margin: 0 0 0.75rem !important;
  letter-spacing: -0.03em !important;
}
.hero-sub {
  font-size: 0.95rem;
  color: var(--text-secondary);
  font-weight: 300;
  max-width: 420px;
  line-height: 1.6;
  letter-spacing: 0.01em;
}

/* ══════════════════════════════
   DETAIL PAGE
══════════════════════════════ */
.detail-poster {
  border-radius: var(--radius-lg);
  overflow: hidden;
  box-shadow: 0 20px 60px rgba(0,0,0,0.8), 0 0 0 1px var(--border-subtle);
  position: relative;
}
.detail-poster img {
  width: 100%;
  display: block;
  border-radius: var(--radius-lg);
}

.detail-meta-pill {
  display: inline-flex;
  align-items: center;
  gap: 0.4rem;
  background: var(--bg-elevated);
  border: 1px solid var(--border-subtle);
  border-radius: 999px;
  padding: 0.3rem 0.9rem;
  font-size: 0.82rem;
  color: var(--text-secondary);
  font-family: var(--font-body);
  font-weight: 400;
}
.detail-meta-pill .pill-icon {
  font-size: 0.85rem;
}
.detail-meta-pills {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
  margin-bottom: 1.8rem;
}

.detail-genre-tag {
  display: inline-block;
  background: rgba(240,192,96,0.08);
  border: 1px solid rgba(240,192,96,0.18);
  border-radius: 4px;
  padding: 0.18rem 0.65rem;
  font-size: 0.75rem;
  color: var(--gold-dim);
  font-family: var(--font-mono);
  font-weight: 400;
  text-transform: uppercase;
  letter-spacing: 0.1em;
  margin: 0.2rem;
}

.overview-text {
  font-size: 1rem;
  color: var(--text-secondary);
  line-height: 1.8;
  font-weight: 300;
  border-left: 2px solid var(--border-glow);
  padding-left: 1.2rem;
  margin: 1rem 0 1.5rem;
  font-style: italic;
}

.rating-badge {
  display: inline-flex;
  align-items: baseline;
  gap: 0.3rem;
  font-family: var(--font-display);
}
.rating-badge .num {
  font-size: 2.4rem;
  font-weight: 700;
  color: var(--gold);
  line-height: 1;
}
.rating-badge .denom {
  font-size: 1rem;
  color: var(--text-muted);
}

/* ══════════════════════════════
   BACK BUTTON
══════════════════════════════ */
.back-btn-wrap .stButton > button {
  background: transparent !important;
  color: var(--text-muted) !important;
  border: 1px solid var(--border-subtle) !important;
  text-transform: none !important;
  letter-spacing: 0.02em !important;
  font-size: 0.85rem !important;
  padding: 0.5rem 1.2rem !important;
  width: auto !important;
}
.back-btn-wrap .stButton > button:hover {
  background: var(--bg-elevated) !important;
  color: var(--text-primary) !important;
  border-color: var(--border-mid) !important;
  box-shadow: none !important;
  transform: none !important;
}

/* ══════════════════════════════
   INFO / WARNING BOXES
══════════════════════════════ */
.stAlert {
  background: var(--bg-surface) !important;
  border: 1px solid var(--border-mid) !important;
  border-radius: var(--radius-md) !important;
  color: var(--text-secondary) !important;
  font-family: var(--font-body) !important;
}

/* ══════════════════════════════
   SCROLLBAR
══════════════════════════════ */
::-webkit-scrollbar { width: 6px; height: 6px; }
::-webkit-scrollbar-track { background: var(--bg-base); }
::-webkit-scrollbar-thumb {
  background: var(--border-mid);
  border-radius: 3px;
}
::-webkit-scrollbar-thumb:hover { background: var(--gold-dim); }

/* ══════════════════════════════
   MISC OVERRIDES
══════════════════════════════ */
.stCaption { color: var(--text-muted) !important; font-family: var(--font-mono) !important; font-size: 0.72rem !important; }
[data-testid="stMarkdownContainer"] p { color: var(--text-secondary) !important; font-family: var(--font-body) !important; }
.element-container { margin-bottom: 0 !important; }
</style>
""", unsafe_allow_html=True)


# =============================
# STATE + ROUTING
# =============================
if "view" not in st.session_state:
    st.session_state.view = "home"
if "selected_tmdb_id" not in st.session_state:
    st.session_state.selected_tmdb_id = None

qp_view = st.query_params.get("view")
qp_id   = st.query_params.get("id")
if qp_view in ("home", "details"):
    st.session_state.view = qp_view
if qp_id:
    try:
        st.session_state.selected_tmdb_id = int(qp_id)
        st.session_state.view = "details"
    except:
        pass


def goto_home():
    st.session_state.view = "home"
    st.query_params["view"] = "home"
    if "id" in st.query_params:
        del st.query_params["id"]
    st.rerun()


def goto_details(tmdb_id: int):
    st.session_state.view     = "details"
    st.session_state.selected_tmdb_id = int(tmdb_id)
    st.query_params["view"]   = "details"
    st.query_params["id"]     = str(int(tmdb_id))
    st.rerun()


# =============================
# API HELPERS
# =============================
@st.cache_data(ttl=30)
def api_get_json(path: str, params: dict | None = None):
    try:
        r = requests.get(f"{API_BASE}{path}", params=params, timeout=25)
        if r.status_code >= 400:
            return None, f"HTTP {r.status_code}: {r.text[:300]}"
        return r.json(), None
    except Exception as e:
        return None, f"Request failed: {e}"


def poster_grid(cards, cols=6, key_prefix="grid"):
    if not cards:
        st.info("No films to display.")
        return

    rows = (len(cards) + cols - 1) // cols
    idx  = 0
    for r in range(rows):
        colset = st.columns(cols, gap="small")
        for c in range(cols):
            if idx >= len(cards):
                break
            m = cards[idx]; idx += 1

            tmdb_id = m.get("tmdb_id")
            title   = m.get("title", "Untitled")
            poster  = m.get("poster_url")

            with colset[c]:
                st.markdown("<div class='cine-card'>", unsafe_allow_html=True)

                if poster:
                    st.markdown(f"<div class='cine-poster-wrap'><img src='{poster}' alt='{title}'/></div>",
                                unsafe_allow_html=True)
                else:
                    st.markdown(
                        "<div class='cine-no-poster'>🎞️<span>No poster</span></div>",
                        unsafe_allow_html=True)

                st.markdown(f"<div class='cine-card-body'><div class='cine-card-title'>{title}</div></div>",
                            unsafe_allow_html=True)

                if st.button("View", key=f"{key_prefix}_{r}_{c}_{idx}_{tmdb_id}"):
                    if tmdb_id:
                        goto_details(tmdb_id)

                st.markdown("</div>", unsafe_allow_html=True)


def to_cards_from_tfidf_items(tfidf_items):
    cards = []
    for x in tfidf_items or []:
        tmdb = x.get("tmdb") or {}
        if tmdb.get("tmdb_id"):
            cards.append({
                "tmdb_id":    tmdb["tmdb_id"],
                "title":      tmdb.get("title") or x.get("title") or "Untitled",
                "poster_url": tmdb.get("poster_url"),
            })
    return cards


def parse_tmdb_search_to_cards(data, keyword: str, limit: int = 24):
    keyword_l = keyword.strip().lower()

    if isinstance(data, dict) and "results" in data:
        raw = data.get("results") or []
        raw_items = []
        for m in raw:
            title      = (m.get("title") or "").strip()
            tmdb_id    = m.get("id")
            poster_path= m.get("poster_path")
            if not title or not tmdb_id:
                continue
            raw_items.append({
                "tmdb_id":      int(tmdb_id),
                "title":        title,
                "poster_url":   f"{TMDB_IMG}{poster_path}" if poster_path else None,
                "release_date": m.get("release_date", ""),
            })
    elif isinstance(data, list):
        raw_items = []
        for m in data:
            tmdb_id   = m.get("tmdb_id") or m.get("id")
            title     = (m.get("title") or "").strip()
            poster_url= m.get("poster_url")
            if not title or not tmdb_id:
                continue
            raw_items.append({
                "tmdb_id":      int(tmdb_id),
                "title":        title,
                "poster_url":   poster_url,
                "release_date": m.get("release_date", ""),
            })
    else:
        return [], []

    matched    = [x for x in raw_items if keyword_l in x["title"].lower()]
    final_list = matched if matched else raw_items

    suggestions = []
    for x in final_list[:10]:
        year  = (x.get("release_date") or "")[:4]
        label = f"{x['title']} ({year})" if year else x["title"]
        suggestions.append((label, x["tmdb_id"]))

    cards = [{"tmdb_id": x["tmdb_id"], "title": x["title"], "poster_url": x["poster_url"]}
             for x in final_list[:limit]]
    return suggestions, cards


# =============================
# SIDEBAR
# =============================
with st.sidebar:
    st.markdown("""
    <div style='padding:0.5rem 0 2rem;'>
      <div style='font-family:"DM Mono",monospace; font-size:0.65rem; letter-spacing:0.22em;
                  text-transform:uppercase; color:#c89840; margin-bottom:0.3rem;'>Est. 2024</div>
      <div style='font-family:"Playfair Display",serif; font-size:1.6rem; font-weight:700;
                  color:#f5ede0; letter-spacing:-0.02em; line-height:1;'>Cinerama</div>
      <div style='width:40px; height:2px; background:linear-gradient(90deg,#f0c060,transparent);
                  margin-top:0.6rem;'></div>
    </div>
    """, unsafe_allow_html=True)

    if st.button("🏠  Home"):
        goto_home()

    st.markdown("<div style='height:1.5rem'></div>", unsafe_allow_html=True)
    st.markdown("<div class='section-label'>Browse</div>", unsafe_allow_html=True)

    home_category = st.selectbox(
        "Feed category",
        ["trending", "popular", "top_rated", "now_playing", "upcoming"],
        index=0,
        format_func=lambda x: x.replace("_", " ").title()
    )

    st.markdown("<div style='height:1rem'></div>", unsafe_allow_html=True)
    grid_cols = st.slider("Columns", 3, 8, 6)

    st.markdown("<div style='height:3rem'></div>", unsafe_allow_html=True)
    st.markdown("""
    <div style='font-family:"DM Mono",monospace; font-size:0.62rem; color:#6a5545;
                letter-spacing:0.08em; line-height:1.9; padding-top:1rem;
                border-top:1px solid rgba(245,200,100,0.06);'>
      POWERED BY<br>
      TF-IDF · TMDB API<br>
      FastAPI · Streamlit
    </div>
    """, unsafe_allow_html=True)


# =============================
# HERO HEADER
# =============================
st.markdown("""
<div class='hero-wrap'>
  <div class='hero-eyebrow'>✦ Cinematic Discovery Engine</div>
  <div class='hero-title'>Find Your Next<br><em>Obsession</em></div>
  <div class='hero-sub'>AI-powered recommendations using TF-IDF similarity matching and live TMDB metadata.</div>
</div>
""", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════
# VIEW: HOME
# ══════════════════════════════════════════════════════════
if st.session_state.view == "home":

    # Search bar
    typed = st.text_input(
        "Search",
        placeholder="Search for a film — try 'inception', 'miyazaki', 'blade runner'...",
        label_visibility="collapsed"
    )

    st.markdown("<div style='height:0.5rem'></div>", unsafe_allow_html=True)

    # ── SEARCH MODE ────────────────────────────────────────
    if typed.strip():
        if len(typed.strip()) < 2:
            st.caption("Type at least 2 characters…")
        else:
            data, err = api_get_json("/tmdb/search", params={"query": typed.strip()})

            if err or data is None:
                st.error(f"Search error: {err}")
            else:
                suggestions, cards = parse_tmdb_search_to_cards(data, typed.strip(), limit=24)

                if suggestions:
                    labels   = ["— Select a title —"] + [s[0] for s in suggestions]
                    selected = st.selectbox("Suggestions", labels, index=0,
                                           label_visibility="collapsed")
                    if selected != "— Select a title —":
                        label_to_id = {s[0]: s[1] for s in suggestions}
                        goto_details(label_to_id[selected])

                st.markdown("<div class='section-label'>Search Results</div>",
                            unsafe_allow_html=True)
                poster_grid(cards, cols=grid_cols, key_prefix="search")
        st.stop()

    # ── HOME FEED ──────────────────────────────────────────
    feed_label = home_category.replace("_", " ").title()
    st.markdown(f"<div class='section-label'>{feed_label}</div>", unsafe_allow_html=True)

    home_cards, err = api_get_json("/home", params={"category": home_category, "limit": 24})
    if err or not home_cards:
        st.error(f"Feed failed: {err or 'Unknown error'}")
        st.stop()

    poster_grid(home_cards, cols=grid_cols, key_prefix="home_feed")


# ══════════════════════════════════════════════════════════
# VIEW: DETAILS
# ══════════════════════════════════════════════════════════
elif st.session_state.view == "details":
    tmdb_id = st.session_state.selected_tmdb_id
    if not tmdb_id:
        st.warning("No film selected.")
        st.button("← Back", on_click=goto_home)
        st.stop()

    # Back button
    st.markdown("<div class='back-btn-wrap'>", unsafe_allow_html=True)
    if st.button("← Back to Discover"):
        goto_home()
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<div style='height:1rem'></div>", unsafe_allow_html=True)

    # Load data
    data, err = api_get_json(f"/movie/id/{tmdb_id}")
    if err or not data:
        st.error(f"Could not load film: {err or 'Unknown error'}")
        st.stop()

    # ── DETAIL LAYOUT ──────────────────────────────────────
    left, right = st.columns([1, 2], gap="large")

    with left:
        st.markdown("<div class='detail-poster'>", unsafe_allow_html=True)
        if data.get("poster_url"):
            st.image(data["poster_url"], use_container_width=True)
        else:
            st.markdown(
                "<div style='aspect-ratio:2/3;background:var(--bg-elevated);display:flex;"
                "align-items:center;justify-content:center;border-radius:20px;"
                "color:var(--text-muted);font-size:3rem;'>🎞️</div>",
                unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    with right:
        title        = data.get("title", "")
        release_date = data.get("release_date", "")
        year         = release_date[:4] if release_date else ""
        vote_avg     = data.get("vote_average")
        genres       = data.get("genres", [])
        overview     = data.get("overview") or "No overview available."

        # Title
        st.markdown(f"""
        <div style='font-family:"Playfair Display",serif; font-size:2.4rem; font-weight:700;
                    color:#f5ede0; line-height:1.1; letter-spacing:-0.02em; margin-bottom:0.3rem;'>
          {title}
        </div>
        """, unsafe_allow_html=True)

        if year:
            st.markdown(f"<div style='font-family:\"DM Mono\",monospace; font-size:0.72rem;"
                        f"color:#c89840; letter-spacing:0.15em; margin-bottom:1.2rem;'>{year}</div>",
                        unsafe_allow_html=True)

        # Pills row
        pills_html = "<div class='detail-meta-pills'>"
        if release_date:
            pills_html += f"<span class='detail-meta-pill'><span class='pill-icon'>📅</span>{release_date}</span>"
        if vote_avg:
            pills_html += f"<span class='detail-meta-pill'><span class='pill-icon'>⭐</span>{vote_avg} / 10</span>"
        pills_html += "</div>"
        st.markdown(pills_html, unsafe_allow_html=True)

        # Genre tags
        if genres:
            genre_html = "".join(
                f"<span class='detail-genre-tag'>{g['name']}</span>"
                for g in genres
            )
            st.markdown(f"<div style='margin-bottom:1.8rem;'>{genre_html}</div>",
                        unsafe_allow_html=True)

        # Rating
        if vote_avg:
            st.markdown(f"""
            <div style='margin-bottom:1.5rem;'>
              <div style='font-family:"DM Sans",sans-serif; font-size:0.7rem; text-transform:uppercase;
                          letter-spacing:0.12em; color:#6a5545; margin-bottom:0.3rem;'>Audience Score</div>
              <div class='rating-badge'>
                <span class='num'>{vote_avg}</span>
                <span class='denom'>/ 10</span>
              </div>
            </div>
            """, unsafe_allow_html=True)

        # Overview
        st.markdown(f"""
        <div style='font-family:"DM Sans",sans-serif; font-size:0.7rem; text-transform:uppercase;
                    letter-spacing:0.12em; color:#6a5545; margin-bottom:0.5rem;'>Synopsis</div>
        <div class='overview-text'>{overview}</div>
        """, unsafe_allow_html=True)

    # Backdrop
    if data.get("backdrop_url"):
        st.markdown("<div style='height:2rem'></div>", unsafe_allow_html=True)
        st.markdown("<div class='section-label'>Backdrop</div>", unsafe_allow_html=True)
        st.markdown(
            f"<img src='{data['backdrop_url']}' style='width:100%;border-radius:12px;"
            f"border:1px solid rgba(245,200,100,0.08);box-shadow:0 12px 40px rgba(0,0,0,0.7);'/>",
            unsafe_allow_html=True)

    # ── RECOMMENDATIONS ────────────────────────────────────
    st.markdown("<div style='height:3rem'></div>", unsafe_allow_html=True)

    title_str = (data.get("title") or "").strip()
    if title_str:
        bundle, err2 = api_get_json(
            "/movie/search",
            params={"query": title_str, "tfidf_top_n": 12, "genre_limit": 12},
        )

        if not err2 and bundle:
            st.markdown("<div class='section-label'>Because You Liked This — Similar Films</div>",
                        unsafe_allow_html=True)
            poster_grid(
                to_cards_from_tfidf_items(bundle.get("tfidf_recommendations")),
                cols=grid_cols, key_prefix="details_tfidf")

            st.markdown("<div style='height:2rem'></div>", unsafe_allow_html=True)
            st.markdown("<div class='section-label'>More In This Genre</div>",
                        unsafe_allow_html=True)
            poster_grid(
                bundle.get("genre_recommendations", []),
                cols=grid_cols, key_prefix="details_genre")
        else:
            st.markdown("<div class='section-label'>Genre Picks</div>", unsafe_allow_html=True)
            genre_only, err3 = api_get_json(
                "/recommend/genre", params={"tmdb_id": tmdb_id, "limit": 18})
            if not err3 and genre_only:
                poster_grid(genre_only, cols=grid_cols, key_prefix="details_genre_fallback")
            else:
                st.info("No recommendations available right now.")
    else:
        st.info("No title available to compute recommendations.")