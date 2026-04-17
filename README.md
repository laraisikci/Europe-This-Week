# 🌍 Europe This Week

> *Tell us how you feel — we'll find the European city that matches your mood right now, based on live events and real weather.*

---

## What is this?

**Europe This Week** is a live, mood-driven travel discovery app built with Streamlit and powered by Cohere LLMs. Unlike traditional travel apps that ask you to pick your interests from a list, this app asks how you're *feeling* this week — and matches you to a European city based on what's actually happening there right now.

The recommendation changes every week because it's driven by live data: real events from Ticketmaster and real weather from Open-Meteo across 15 European cities.

---

## How it works

### 1. 🎭 Set your mood
Move 5 sliders to describe how you're feeling this week:
- 🔋 **Energy Level** — Exhausted vs. Buzzing with energy
- 👥 **Social Appetite** — Solo & quiet vs. Meet people & party
- 💸 **Budget Mood** — Watching every euro vs. Ready to splash out
- ☀️ **Sunshine Craving** — Cozy indoors vs. Need that sun
- 🧗 **Adventure Appetite** — Take it easy vs. Craving adrenaline

### 2. 🗺️ Live Europe Mood Map
The app fetches live data for all 15 cities before making any recommendation:
- **Ticketmaster API** — number of events happening this week in each city
- **Open-Meteo API** — current temperature and weather conditions

This data is visualized on an interactive map of Europe where bubble size = live events and color = current temperature.

### 3. 🎯 Mood-matched recommendation
A scoring model combines your slider values with live event density and live weather alignment to recommend the city that best fits your mood *this week specifically*.

### 4. ✨ AI-powered travel narrative
Cohere LLM generates a personalized explanation grounded in the live data — referencing the actual weather and events happening in your recommended city right now.

### 5. 🤖 Multi-agent debate
Three AI agents with different travel personas independently evaluate your top 3 cities:
- 🎒 **Budget Traveler** — focused on value for money
- 👑 **Luxury Traveler** — focused on premium experiences
- 🧗 **Adventure Seeker** — focused on outdoor activity

A neutral **Moderator** then reads all three verdicts and delivers a final synthesized recommendation with a confidence level (High / Medium / Low).

### 6. 💬 Travel chatbot
A personalized travel assistant answers your questions about the recommended city, aware of your mood profile and the live weather conditions.

---

## Tech Stack

| Component | Technology |
|-----------|------------|
| Frontend | Streamlit |
| LLM | Cohere `command-r-plus-08-2024` |
| Live events | Ticketmaster Discovery API |
| Live weather | Open-Meteo API (free, no key needed) |
| Charts & maps | Plotly |
| Data processing | Pandas |

---

## Running locally

**1. Clone the repo:**
```bash
git clone https://github.com/laraisikci/EventfulTravelApp.git
cd EventfulTravelApp
```

**2. Install dependencies:**
```bash
pip install streamlit pandas requests plotly cohere
```

**3. Add your API keys — create this file:**
```
.streamlit/secrets.toml
```
With the following contents:
```toml
COHERE_API_KEY = "your-cohere-key-here"
TICKETMASTER_API_KEY = "your-ticketmaster-key-here"
```

**4. Run the app:**
```bash
streamlit run app.py
```

Then open your browser at `http://localhost:8501`

---

## Live Demo

🔗 [Open the app on Streamlit Cloud](https://your-streamlit-url.streamlit.app)

---

## Cities covered

Barcelona · Paris · Amsterdam · Naples · Ljubljana · Ghent · Mallorca · Chamonix · Lisbon · Reykjavik · Dubrovnik · Prague · Seville · Vienna · Algarve

---

## ⚠️ Limitations

- Only 15 pre-selected European cities are covered
- Slider-to-vibe mapping uses rule-based thresholds, not learned preferences
- Weather shows current conditions, not a forecast for your travel dates
- Ticketmaster coverage varies by city
- Flight cost estimates are approximate and do not reflect real-time availability
- AI agent personas reflect LLM training knowledge, not real user reviews

---

## Built for

ESADE Master in Business Analytics (MIBA) — Prototyping Products with Data and AI course

*Assignments 1, 2 & 3 — iterative prototype development*
