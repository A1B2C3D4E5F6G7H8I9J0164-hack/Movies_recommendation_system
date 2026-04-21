# 🎞️ Cinerama — Premium Movie Recommendation Engine

Cinerama is an AI-powered cinematic discovery engine. Built with a decoupled **FastAPI** backend and a beautiful, high-contrast **Streamlit** frontend, Cinerama calculates personalized content-based movie recommendations using machine learning (TF-IDF vectorization) while pulling dynamic, real-time metadata (posters, genres, ratings, and backdrops) straight from the TMDB API.

---

## 📸 Interface Preview

*(A sleek, "Midnight Cinema" dark-themed UI featuring Playfair Display and DM Sans, custom styling, film grain overlays, responsive theater cards, and lightning-fast search autocomplete).*

## 🌟 Key Features

- **🧠 Machine Learning Core:** Utilizes `scikit-learn` for Term Frequency-Inverse Document Frequency (TF-IDF) calculations against a robust dataset of movie attributes (tags, cast, crew) to generate highly accurate "Because you liked..." suggestions.
- **⚡ Async Backend:** Powered by `FastAPI` to instantly serve similarity matrices loaded from optimized Pickle files into server memory.
- **🎨 Luxury UI/UX Design:** A completely overhauled Streamlit interface utilizing raw CSS injection for a cinematic dark-mode experience, overriding default constraints to provide a professional layout.
- **📡 Live Data Integration:** Interacts directly with the TMDB API to enrich local machine-learning predictions with high-resolution localized posters and accurate, up-to-the-minute synopses and audience scores.
- **🔍 Auto-complete Filtering:** Highly responsive local search logic preventing excessive API hitting while delivering ultra-fast search results. 

## 🛠️ Technology Stack

- **Backend / Data Science:** Python, FastAPI, Pandas, Scikit-learn, Numpy, Scipy.
- **Frontend / UI:** Streamlit, Vanilla HTML/CSS, Google Fonts.
- **Infrastructure:** Uvicorn, Python-Dotenv, Render.

---

## 🚀 Local Development

### 1. Clone the repository and setup environment
```bash
git clone https://github.com/A1B2C3D4E5F6G7H8I9J0164-hack/Movies_recommendation_system.git
cd Movies_recommendation_system
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### 2. Configure TMDB API Key
Create a `.env` file in the root directory and add your key:
```env
TMDB_API_KEY=your_api_key_here
```

### 3. Run the application
Because Cinerama utilizes a microservice architecture, you must run both pieces of the stack simultaneously.

**Launch the FastAPI Backend:**
Open a terminal window and run:
```bash
uvicorn main:app --reload
```
*The backend will boot up on `http://127.0.0.1:8000` and deserialize the NumPy recommendation models into memory.*

**Launch the Streamlit Frontend:**
Open a second terminal window (ensure your `.venv` is activated) and run:
```bash
streamlit run app.py
```
*Your browser will automatically open to `http://localhost:8501`.*

---

## ☁️ Deployment (Render)

This project is tailored for deployment on **Render.com**. It uses two separate Web Services.

### Environment Requirements
- Ensure your repository contains a `.python-version` file defining `3.11.9`.
- **Backend Environment Vairables:** Set `TMDB_API_KEY` on your backend Render service.

### Deployment Commands
1. **Backend Web Service:**
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `uvicorn main:app --host 0.0.0.0 --port $PORT`
2. **Frontend Web Service:**
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `streamlit run app.py --server.port $PORT --server.address 0.0.0.0`
   - *Note: Remember to update `API_BASE` in `app.py` to point to the live Render backend URL before deploying the frontend.*

---

## 📂 Project Structure

```bash
├── app.py                  # Streamlit application (Frontend)
├── main.py                 # FastAPI server (Backend)
├── .env                    # Secret configurations (Ignored dynamically)
├── requirements.txt        # Production dependencies
├── .python-version         # Python version control for Render
├── df.pkl                  # Dataframe serializations
├── indices.pkl             # Reference mappings
├── tfidf.pkl               # Trained TF-IDF Vectorizer
└── tfidf_matrix.pkl        # Compressed distance calculations
```
