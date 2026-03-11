import streamlit as st
import pandas as pd
import requests
import plotly.express as px
import plotly.graph_objects as go

# ── Page Config ────────────────────────────────────────────────────────────────
st.set_page_config(page_title="Eventful Travel App", layout="wide", page_icon="✈️")

# ── CITY DATABASE ──────────────────────────────────────────────────────────────
# Each city has: vibe scores (0-3), interest scores (0-3), distance zone, base cost
CITY_DATA = {
    "Barcelona, Spain": {
        "vibes": {"Beach": 3, "Nightlife": 3, "Culture": 2, "Foodie": 2, "Adventure": 1, "Relaxation": 1, "Romantic": 2, "Hidden Gems": 0},
        "interests": {"Music Festivals": 3, "Art Galleries": 2, "Sports": 1, "Hiking": 1, "Foodie Tours": 2},
        "distance_zone": 1, "base_flight": 80, "description": "💃 Sun, Gaudí, and the best nightlife in Southern Europe.",
    },
    "Paris, France": {
        "vibes": {"Romantic": 3, "Culture": 3, "Foodie": 3, "Hidden Gems": 1, "Relaxation": 1, "Nightlife": 1, "Beach": 0, "Adventure": 0},
        "interests": {"Art Galleries": 3, "Music Festivals": 1, "Sports": 1, "Hiking": 0, "Foodie Tours": 3},
        "distance_zone": 1, "base_flight": 100, "description": "🗼 Romance, world-class cuisine, and iconic art museums.",
    },
    "Amsterdam, Netherlands": {
        "vibes": {"Nightlife": 3, "Culture": 2, "Hidden Gems": 2, "Romantic": 2, "Foodie": 1, "Relaxation": 1, "Beach": 0, "Adventure": 1},
        "interests": {"Music Festivals": 3, "Art Galleries": 2, "Sports": 1, "Hiking": 0, "Foodie Tours": 1},
        "distance_zone": 1, "base_flight": 90, "description": "🎧 World-class DJs, canals, and vibrant cultural scene.",
    },
    "Naples, Italy": {
        "vibes": {"Foodie": 3, "Culture": 2, "Hidden Gems": 2, "Beach": 2, "Romantic": 1, "Relaxation": 2, "Nightlife": 1, "Adventure": 0},
        "interests": {"Foodie Tours": 3, "Art Galleries": 2, "Music Festivals": 1, "Sports": 1, "Hiking": 1},
        "distance_zone": 1, "base_flight": 90, "description": "🍕 The birthplace of pizza with authentic markets and history.",
    },
    "Ljubljana, Slovenia": {
        "vibes": {"Relaxation": 3, "Hidden Gems": 3, "Culture": 2, "Romantic": 2, "Adventure": 1, "Foodie": 1, "Nightlife": 0, "Beach": 0},
        "interests": {"Hiking": 2, "Art Galleries": 1, "Foodie Tours": 2, "Music Festivals": 0, "Sports": 1},
        "distance_zone": 1, "base_flight": 85, "description": "🍃 Europe's hidden gem — peaceful, green, and charming.",
    },
    "Ghent, Belgium": {
        "vibes": {"Culture": 3, "Hidden Gems": 3, "Foodie": 2, "Romantic": 2, "Relaxation": 2, "Nightlife": 1, "Beach": 0, "Adventure": 0},
        "interests": {"Art Galleries": 3, "Foodie Tours": 2, "Music Festivals": 2, "Sports": 0, "Hiking": 0},
        "distance_zone": 1, "base_flight": 95, "description": "🏰 Medieval architecture, craft beer, and an art scene.",
    },
    "Mallorca, Spain": {
        "vibes": {"Beach": 3, "Relaxation": 3, "Romantic": 2, "Foodie": 1, "Nightlife": 2, "Adventure": 1, "Culture": 1, "Hidden Gems": 1},
        "interests": {"Hiking": 2, "Foodie Tours": 1, "Music Festivals": 1, "Art Galleries": 0, "Sports": 2},
        "distance_zone": 1, "base_flight": 100, "description": "🏖️ Crystal clear water, hidden coves, and coastal bliss.",
    },
    "Chamonix, France": {
        "vibes": {"Adventure": 3, "Relaxation": 1, "Hidden Gems": 2, "Romantic": 2, "Culture": 1, "Nightlife": 0, "Beach": 0, "Foodie": 1},
        "interests": {"Hiking": 3, "Sports": 3, "Art Galleries": 0, "Foodie Tours": 0, "Music Festivals": 0},
        "distance_zone": 1, "base_flight": 110, "description": "⛰️ Alpine adventure capital — hiking, skiing, and mountain air.",
    },
    "Lisbon, Portugal": {
        "vibes": {"Culture": 3, "Foodie": 2, "Romantic": 2, "Hidden Gems": 2, "Relaxation": 2, "Nightlife": 2, "Beach": 1, "Adventure": 0},
        "interests": {"Art Galleries": 2, "Foodie Tours": 3, "Music Festivals": 2, "Hiking": 1, "Sports": 1},
        "distance_zone": 1, "base_flight": 95, "description": "🎵 Fado music, pastel de nata, and stunning hilltop views.",
    },
    "Reykjavik, Iceland": {
        "vibes": {"Adventure": 3, "Hidden Gems": 3, "Relaxation": 2, "Romantic": 2, "Culture": 1, "Nightlife": 1, "Beach": 0, "Foodie": 0},
        "interests": {"Hiking": 3, "Art Galleries": 1, "Music Festivals": 1, "Sports": 2, "Foodie Tours": 0},
        "distance_zone": 2, "base_flight": 180, "description": "🌌 Northern lights, geysers, and raw volcanic landscapes.",
    },
    "Dubrovnik, Croatia": {
        "vibes": {"Beach": 3, "Romantic": 3, "Culture": 2, "Hidden Gems": 2, "Relaxation": 2, "Nightlife": 1, "Adventure": 1, "Foodie": 1},
        "interests": {"Art Galleries": 1, "Hiking": 2, "Foodie Tours": 2, "Music Festivals": 1, "Sports": 1},
        "distance_zone": 1, "base_flight": 120, "description": "🏰 Game of Thrones' King's Landing — stunning walls and Adriatic sea.",
    },
    "Prague, Czech Republic": {
        "vibes": {"Culture": 3, "Hidden Gems": 2, "Nightlife": 3, "Romantic": 2, "Foodie": 1, "Relaxation": 1, "Beach": 0, "Adventure": 0},
        "interests": {"Art Galleries": 2, "Music Festivals": 2, "Foodie Tours": 1, "Sports": 0, "Hiking": 0},
        "distance_zone": 1, "base_flight": 85, "description": "🍺 Fairytale architecture, cheap beer, and buzzing nightlife.",
    },
    "Seville, Spain": {
        "vibes": {"Culture": 3, "Foodie": 3, "Romantic": 3, "Nightlife": 2, "Hidden Gems": 1, "Relaxation": 1, "Beach": 0, "Adventure": 0},
        "interests": {"Art Galleries": 2, "Foodie Tours": 3, "Music Festivals": 2, "Sports": 1, "Hiking": 0},
        "distance_zone": 1, "base_flight": 90, "description": "💃 Flamenco, tapas, and Moorish palaces under the Andalusian sun.",
    },
    "Vienna, Austria": {
        "vibes": {"Culture": 3, "Romantic": 3, "Relaxation": 2, "Foodie": 2, "Hidden Gems": 1, "Nightlife": 1, "Beach": 0, "Adventure": 0},
        "interests": {"Art Galleries": 3, "Music Festivals": 3, "Foodie Tours": 2, "Sports": 0, "Hiking": 0},
        "distance_zone": 1, "base_flight": 105, "description": "🎻 Classical music, imperial palaces, and Viennese coffee culture.",
    },
    "Algarve, Portugal": {
        "vibes": {"Beach": 3, "Relaxation": 3, "Romantic": 2, "Adventure": 1, "Foodie": 1, "Hidden Gems": 1, "Nightlife": 1, "Culture": 0},
        "interests": {"Hiking": 2, "Sports": 2, "Foodie Tours": 1, "Art Galleries": 0, "Music Festivals": 0},
        "distance_zone": 1, "base_flight": 100, "description": "🌊 Dramatic cliffs, golden beaches, and fresh seafood.",
    },
}

# ── SCORING MODEL ──────────────────────────────────────────────────────────────

def score_cities(vibes, interests, activity_level):
    """
    Scores every city based on vibe match + interest match.
    Activity level adds a multiplier to adventure/relaxation scores.
    Returns a sorted DataFrame with scores and breakdown.
    """
    activity_multiplier = {"Very Low": 0.5, "Moderate": 1.0, "Intense": 1.5}
    mult = activity_multiplier[activity_level]

    results = []
    for city, data in CITY_DATA.items():
        vibe_score = sum(data["vibes"].get(v, 0) for v in vibes)
        # Apply activity multiplier to adventure/relaxation specifically
        if "Adventure" in vibes:
            vibe_score += data["vibes"].get("Adventure", 0) * (mult - 1)
        if "Relaxation" in vibes:
            vibe_score += data["vibes"].get("Relaxation", 0) * (0.5 - mult if mult < 1 else 0)

        interest_score = sum(data["interests"].get(i, 0) for i in interests)
        total = vibe_score + interest_score
        max_possible = len(vibes) * 3 + len(interests) * 3 if (vibes or interests) else 1
        match_pct = min(round((total / max_possible) * 100), 99) if max_possible > 0 else 0

        results.append({
            "city": city,
            "vibe_score": round(vibe_score, 1),
            "interest_score": round(interest_score, 1),
            "total_score": round(total, 1),
            "match_pct": match_pct,
            "description": data["description"],
        })

    df = pd.DataFrame(results).sort_values("total_score", ascending=False).reset_index(drop=True)
    return df

# ── COST MODEL ─────────────────────────────────────────────────────────────────

def estimate_cost(city_name, budget, travel_dates, activity_level):
    """
    Estimates cost based on: base flight price, distance zone,
    travel season (peak/off-peak), and activity level.
    """
    data = CITY_DATA.get(city_name, {})
    base_flight = data.get("base_flight", 120)
    zone = data.get("distance_zone", 1)

    # Season multiplier
    season_mult = 1.0
    if travel_dates and len(travel_dates) >= 1:
        month = travel_dates[0].month
        if month in [6, 7, 8, 12]:  # Peak season
            season_mult = 1.35
        elif month in [4, 5, 9, 10]:  # Shoulder
            season_mult = 1.1

    # Activity level affects accommodation/activities spend
    activity_spend = {"Very Low": 40, "Moderate": 70, "Intense": 110}
    est_activities = activity_spend[activity_level]

    est_flight = round(base_flight * zone * season_mult)
    total = est_flight + est_activities
    affordable = total <= budget
    season_label = "Peak season 🔴" if season_mult == 1.35 else ("Shoulder season 🟡" if season_mult == 1.1 else "Off-peak season 🟢")

    return est_flight, est_activities, total, affordable, season_label

# ── TICKETMASTER ───────────────────────────────────────────────────────────────

def fetch_real_events(city_name):
    clean_city = city_name.split(',')[0].strip()
    api_key = st.secrets.get("TICKETMASTER_API_KEY", "9Rri7l1kutIcmyOqcbKstEN88GkcPGy7")
    url = f"https://app.ticketmaster.com/discovery/v2/events.json?city={clean_city}&apikey={api_key}&size=4"
    try:
        response = requests.get(url, timeout=5)
        data = response.json()
        if "_embedded" in data:
            return data['_embedded']['events'][:4]
        return []
    except:
        return []

# ── STYLING ────────────────────────────────────────────────────────────────────

st.markdown("""
    <style>
    .main { background-color: #f5f7f9; }
    .stButton>button {
        background-color: #FF4B4B; color: white;
        border-radius: 20px; height: 3em; width: 100%; font-weight: bold;
    }
    .recommendation-card {
        padding: 20px; border-radius: 15px; background-color: #ffffff;
        border-left: 10px solid #FF4B4B;
        box-shadow: 2px 2px 10px rgba(0,0,0,0.1); margin-bottom: 20px;
    }
    .alt-card {
        padding: 12px; border-radius: 10px; background-color: #f0f4ff;
        border-left: 5px solid #4B7BFF; margin-bottom: 10px;
    }
    </style>
""", unsafe_allow_html=True)

# ── HEADER ─────────────────────────────────────────────────────────────────────

st.markdown("<h1 style='text-align:center;color:#FF4B4B;'>🌍 Eventful Travel App</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center;font-size:18px;'>Find your next adventure based on your unique vibe.</p>", unsafe_allow_html=True)
st.divider()

# ── SIDEBAR ────────────────────────────────────────────────────────────────────

with st.sidebar:
    st.header("📍 Travel Details")
    travel_dates = st.date_input("When are you free?", [])
    budget = st.slider("Max Flight Budget (€)", 50, 1000, 300)
    st.header("🎨 Personal Interests")
    interests = st.multiselect(
        "What do you love?",
        ["Music Festivals", "Art Galleries", "Sports", "Hiking", "Foodie Tours"]
    )

# ── MAIN INPUTS ────────────────────────────────────────────────────────────────

st.subheader("What's the mood of this trip?")
col_v, col_a = st.columns(2)

with col_v:
    vibes = st.multiselect(
        "Trip Vibe:",
        ["Relaxation", "Adventure", "Nightlife", "Culture", "Hidden Gems", "Romantic", "Foodie", "Beach"],
        default=["Culture"]
    )
with col_a:
    activity_level = st.select_slider(
        "Desired activity level:",
        options=["Very Low", "Moderate", "Intense"]
    )

st.divider()

# ── MAIN LOGIC ─────────────────────────────────────────────────────────────────

if st.button("✨ SURPRISE ME ✨"):
    if not vibes and not interests:
        st.warning("Please select at least one vibe or interest to get a recommendation!")
        st.stop()

    scores_df = score_cities(vibes, interests, activity_level)
    top = scores_df.iloc[0]
    city = top["city"]

    est_flight, est_act, total_est, affordable, season_label = estimate_cost(
        city, budget, travel_dates, activity_level
    )
    real_events = fetch_real_events(city)

    st.balloons()

    # ── Recommendation Card ──
    st.markdown(f"""
    <div class="recommendation-card">
        <h2 style='color:#FF4B4B;'>Pack your bags for {city}!</h2>
        <p style='font-size:18px;'>{top['description']}</p>
        <p style='font-size:15px;color:#888;'>Match score: <b>{top['match_pct']}%</b> based on your selected vibes and interests</p>
    </div>
    """, unsafe_allow_html=True)

    # ── Two columns: Score breakdown + Cost ──
    col_left, col_right = st.columns(2)

    with col_left:
        st.write("### 🎯 Why this destination?")
        breakdown_data = {
            "Category": ["Vibe Match", "Interest Match"],
            "Score": [top["vibe_score"], top["interest_score"]]
        }
        fig = px.bar(
            breakdown_data, x="Category", y="Score",
            color="Category", color_discrete_sequence=["#FF4B4B", "#4B7BFF"],
            title="Score Breakdown"
        )
        fig.update_layout(showlegend=False, height=280)
        st.plotly_chart(fig, use_container_width=True)

    with col_right:
        st.write("### 💰 Cost Estimate")
        st.caption(f"Travel season: {season_label}")
        c1, c2, c3 = st.columns(3)
        budget_diff = budget - total_est
        status = "Under Budget ✅" if affordable else "Over Budget ⚠️"
        c1.metric("Est. Flight", f"€{est_flight}")
        c2.metric("Activities", f"€{est_act}")
        c3.metric("Total", f"€{total_est}", delta=f"€{abs(budget_diff)} {status}")
        if not affordable:
            st.warning("This trip slightly exceeds your budget. Consider travelling in off-peak season!")
        else:
            st.success("This trip fits within your budget!")

    st.divider()

    # ── Top 3 Alternatives ──
    st.write("### 🗺️ Other destinations you might love")
    alternatives = scores_df.iloc[1:4]
    alt_cols = st.columns(3)
    for i, (_, row) in enumerate(alternatives.iterrows()):
        with alt_cols[i]:
            st.markdown(f"""
            <div class="alt-card">
                <b>{row['city']}</b><br>
                <span style='color:#4B7BFF;font-size:13px;'>{row['match_pct']}% match</span><br>
                <span style='font-size:12px;color:#555;'>{row['description']}</span>
            </div>
            """, unsafe_allow_html=True)

    # ── All City Scores Chart ──
    with st.expander("📊 See full ranking of all destinations"):
        fig2 = px.bar(
            scores_df, x="match_pct", y="city", orientation="h",
            color="match_pct", color_continuous_scale="Reds",
            labels={"match_pct": "Match %", "city": "Destination"},
            title="All Destinations Ranked by Match Score"
        )
        fig2.update_layout(height=500, yaxis={"categoryorder": "total ascending"})
        st.plotly_chart(fig2, use_container_width=True)

    st.divider()

    # ── Live Events ──
    if real_events:
        st.subheader(f"🎭 Live Events in {city.split(',')[0]}")
        cols = st.columns(len(real_events))
        for i, event in enumerate(real_events):
            with cols[i]:
                event_name = event.get('name', 'Event')
                event_date = event.get('dates', {}).get('start', {}).get('localDate', 'TBD')
                event_url = event.get('url', '#')
                st.info(f"**{event_name}**")
                st.caption(f"📅 {event_date}")
                st.link_button("View Tickets 🎟️", event_url)
    else:
        st.warning("No live events found for this location right now.")
