# 🧠 EmoSense — AI Emotion Detection from Text

> Project #29 from the AI Mini-Projects list
> Built with: **React + Vite + Tailwind CSS v4 + Python (Naive Bayes)**

---

## 📌 Purpose of the Project

**EmoSense** is a web application that analyzes any piece of text and identifies the emotions expressed within it. Instead of giving a simple "positive/negative" sentiment label, EmoSense goes deeper — it maps text to **8 primary emotions** based on **Plutchik's Wheel of Emotions** (a well-known psychological model):

> Joy · Sadness · Anger · Fear · Surprise · Disgust · Anticipation · Trust

**Why does this matter?**
- Customer feedback analysis (understand *how* users feel, not just *if* they're satisfied)
- Mental health journaling (detect emotional patterns over time)
- Social media monitoring (understand emotional trends in posts)
- Content moderation (flag emotionally extreme or harmful content)
- HR tools (analyze employee feedback with nuance)

---

## 🔧 Tech Stack

| Layer | Technology |
|---|---|
| Frontend Framework | React 19 |
| Build Tool | Vite 6 |
| Styling | Tailwind CSS v4 (@tailwindcss/vite plugin) |
| ML Model | Naive Bayes + TF-IDF Vectorizer |
| ML Libraries | Scikit-learn · Pandas · NumPy · Matplotlib · Seaborn |
| Fonts | Syne + DM Sans (Google Fonts) |

---

## 🏗️ Workflow / How I Built It

### Step 1 — Project Setup (Vite + Tailwind v4)
Following the official Tailwind CSS v4 Vite guide:
```bash
npm create vite@latest emotion-detector -- --template react
cd emotion-detector
npm install tailwindcss @tailwindcss/vite
```

In vite.config.js, added the Tailwind Vite plugin (no separate tailwind.config.js needed in v4):
```js
import tailwindcss from '@tailwindcss/vite'
// plugins: [react(), tailwindcss()]
```

In src/index.css:
```css
@import "tailwindcss";
```

### Step 2 — Machine Learning Model (Python)
Built a Naive Bayes classifier to classify text into 8 emotion categories:

- Created a dataset of **400 labeled sentences** (50 per emotion)
- Used **TF-IDF Vectorizer** with bigrams (ngram_range=(1,2)) to convert text to numbers
- Trained a **Multinomial Naive Bayes** model using Scikit-learn
- Achieved **~67% cross-validation accuracy** across 5 folds
- Evaluated using confusion matrix, classification report, and per-emotion F1 scores
- Saved the trained model as emotion_model.pkl using pickle
```python
pipeline = Pipeline([
    ('tfidf', TfidfVectorizer(ngram_range=(1, 2), max_features=8000)),
    ('nb', MultinomialNB(alpha=0.3))
])
pipeline.fit(X_train, y_train)
```

### Step 3 — Emotion Detection Logic (Frontend)
Built a custom keyword-based NLP engine in JavaScript:

- **Weighted keyword map** with 3 tiers (high / medium / low weight) for all 8 emotions
- **Negation detection** — "not happy" correctly detects sadness
- **Punctuation boosters** — multiple !!! boosts anger/surprise, ... boosts sadness
- **CAPS detection** — HOW DARE YOU correctly detects anger
- Works **completely offline** — no internet or API key required

### Step 4 — UI Design
Designed a dark-mode interface with:
- **Emotion Orb** — animated glowing sphere that changes color per emotion
- **Score Bars** — animated bars for all 8 emotions, color-coded
- **Insight Panel** — one-sentence explanation of the emotional pattern
- **Tags** — showing sentiment, intensity level and tone word
- **Sample Texts** — 6 pre-written examples to try instantly
- **History Panel** — tracks recent analyses (last 10)

### Step 5 — UX Polish
- Character count limit (500 chars)
- Loading state with spinner animation
- Responsive layout using CSS Grid
- Smooth fade-up animations for results
- Ambient background blobs that shift color based on detected emotion

---

## 🚀 How to Run Locally

### Web App
```bash
# 1. Go into the project folder
cd emotion-detector

# 2. Install dependencies
npm install

# 3. Start the dev server
npm run dev

# 4. Open in browser
http://localhost:5173
```

### ML Training Model (Python)
```bash
# 1. Install Python libraries
pip install scikit-learn matplotlib seaborn pandas numpy

# 2. Run the training script
python train_model.py
```

This will generate:
- emotion_model.pkl — saved trained model
- emotion_classifier_results.png — confusion matrix and F1 chart

---

## 📁 Project Structure
emotion-detector/
├── index.html                        # Entry HTML
├── vite.config.js                    # Vite + Tailwind v4 setup
├── package.json                      # Dependencies
├── README.md                         # This file
├── train_model.py                    # Naive Bayes training code
├── emotion_model.pkl                 # Trained model (generated)
├── emotion_classifier_results.png    # Evaluation charts (generated)
└── src/
    ├── App.jsx                       # Main UI + emotion detection logic
    ├── main.jsx                      # React root
    └── index.css                     # Tailwind v4 + animations
---

## 🧪 Sample Inputs to Try

1. "I just got promoted! This is the best day of my life!" → Joy (high)
2. "I can't believe they canceled my favorite show..." → Sadness (medium)
3. "The deadline is tomorrow and I haven't started" → Fear (high)
4. "How dare they do this to me!!" → Anger (high)
5. "Ew, that is absolutely revolting." → Disgust (medium)
6. "It's just another ordinary Tuesday." → Neutral (low)

---

## 📊 ML Model Results

| Metric | Score |
|---|---|
| Dataset Size | 400 sentences |
| Emotions | 8 categories |
| Algorithm | Multinomial Naive Bayes |
| Vectorizer | TF-IDF (bigrams) |
| CV Accuracy | ~67% (5-fold) |

---

## 🔮 Future Improvements

- Upgrade to BERT or RoBERTa for deeper context understanding
- Add multilingual support (Tamil and Hindi)
- Build an emotion timeline dashboard for full conversations
- Deploy as a REST API using Flask or FastAPI
- Add voice input using Web Speech API

---

## 🎓 Learning Outcomes

- Setting up Tailwind CSS v4 with Vite (plugin-based, no config file)
- Training and evaluating a Naive Bayes text classification model
- Building a weighted keyword NLP engine with negation detection
- Creating data-driven visualizations (animated bars, dynamic color themes)
- Designing a dark UI with glassmorphism, glow effects and ambient backgrounds

---

*Built as part of AI Mini-Projects assignment · March 2026*
*B.Tech Information Technology · KPR Institute of Engineering and Technology*
