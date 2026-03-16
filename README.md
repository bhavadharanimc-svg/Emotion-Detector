# 🧠 EmoSense — AI Emotion Detection from Text

> Project #29 from the AI Mini-Projects list  
> Built with: **React + Vite + Tailwind CSS v4 + Claude AI (Anthropic API)**

---

## 📌 Purpose of the Project

**EmoSense** is an AI-powered web application that analyzes any piece of text and identifies the emotions expressed within it. Instead of giving a simple "positive/negative" sentiment label, EmoSense goes deeper — it maps text to **8 primary emotions** based on **Plutchik's Wheel of Emotions** (a well-known psychological model):

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
| Build Tool | **Vite 6** (via `npm create vite`) |
| Styling | **Tailwind CSS v4** (using `@tailwindcss/vite` plugin) |
| AI Model | **Claude claude-sonnet-4-20250514** via Anthropic API |
| Fonts | Syne (display) + DM Sans (body) from Google Fonts |

---

## 🏗️ Workflow / How I Built It

### Step 1 — Project Setup (Vite + Tailwind v4)
Following the official [Tailwind CSS v4 Vite guide](https://tailwindcss.com/docs/installation/using-vite):

```bash
npm create vite@latest emotion-detector -- --template react
cd emotion-detector
npm install tailwindcss @tailwindcss/vite
```

In `vite.config.js`, added the Tailwind Vite plugin (no separate `tailwind.config.js` needed in v4):
```js
import tailwindcss from '@tailwindcss/vite'
// added to plugins: [react(), tailwindcss()]
```

In `src/index.css`:
```css
@import "tailwindcss";
```

### Step 2 — UI Design
Designed a dark-mode interface with:
- **Emotion Orb**: An animated, glowing sphere that changes color based on the detected primary emotion
- **Score Bars**: Animated horizontal bars for all 8 emotions with color-coded visualization
- **Insight Panel**: AI-generated one-sentence explanation of the emotional pattern
- **Sample Texts**: 6 pre-written examples to try instantly
- **History Panel**: Keeps track of recent analyses (last 10)

### Step 3 — Claude API Integration
Used the `/v1/messages` endpoint with a carefully crafted **system prompt** that:
- Instructs Claude to use Plutchik's 8-emotion model
- Returns a strict JSON schema (no markdown, no extra text)
- Asks for: primary emotion, per-emotion scores (0–100), intensity level, sentiment, tone word, insight sentence, and emotional keywords

```js
const response = await fetch('https://api.anthropic.com/v1/messages', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    model: 'claude-sonnet-4-20250514',
    max_tokens: 1000,
    system: systemPrompt,
    messages: [{ role: 'user', content: `Analyze this text: "${text}"` }]
  })
})
```

### Step 4 — Dynamic Visualization
Each emotion has a defined color, emoji, glow effect, and gradient. When a result arrives:
- The **orb animates** into the primary emotion's color with a pulsing glow
- Score bars animate from 0% width to their target width (CSS animation)
- Background ambient blobs shift to reflect the emotional color palette

### Step 5 — UX Polish
- Character count limit (500 chars)
- Loading state with spinner
- Error handling for API failures
- Responsive layout with CSS Grid
- Smooth fade-up animations for results

---

## 🚀 How to Run Locally

```bash
# 1. Clone / download the project
cd emotion-detector

# 2. Install dependencies
npm install

# 3. Start the dev server
npm run dev

# 4. Open http://localhost:5173
```

> **Note:** The app uses the Anthropic API via the browser. In production, proxy API calls through a backend to protect your API key.

---

## 📁 Project Structure

```
emotion-detector/
├── index.html              # Entry HTML (fonts, title)
├── vite.config.js          # Vite + Tailwind v4 plugin setup
├── package.json
└── src/
    ├── main.jsx            # React root
    ├── index.css           # Tailwind v4 import + custom animations
    └── App.jsx             # Main app (UI + Claude API logic)
```

---

## 🧪 Sample Inputs to Try

1. *"I just got promoted! This is the best day of my life!"* → **Joy** (high intensity)
2. *"I can't believe they canceled my favorite show..."* → **Sadness** (medium)
3. *"The deadline is tomorrow and I haven't started"* → **Fear** (high)
4. *"It's just another ordinary Tuesday."* → **Neutral** (low)

---

## 🎓 Learning Outcomes

- Setting up **Tailwind CSS v4** with Vite (new plugin-based approach, no config file)
- Making **direct API calls** to Claude from a React frontend
- **Prompt engineering** for structured JSON output
- Building **data-driven visualizations** (animated bars, dynamic color themes)
- Designing **dark UI** with glassmorphism, glow effects, and ambient backgrounds

---

*Built as part of AI Mini-Projects assignment · March 2026*
