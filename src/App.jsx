import { useState, useRef, useEffect } from 'react'

// ─── Emotion Config ────────────────────────────────────────────────────
const EMOTIONS = {
  joy:        { emoji: '😄', label: 'Joy',        color: '#facc15', glow: 'rgba(250,204,21,0.4)',  bg: 'from-yellow-400/20 to-amber-300/5'  },
  sadness:    { emoji: '😢', label: 'Sadness',    color: '#60a5fa', glow: 'rgba(96,165,250,0.4)',  bg: 'from-blue-400/20 to-indigo-400/5'   },
  anger:      { emoji: '😠', label: 'Anger',      color: '#f87171', glow: 'rgba(248,113,113,0.4)', bg: 'from-red-400/20 to-rose-400/5'      },
  fear:       { emoji: '😨', label: 'Fear',       color: '#a78bfa', glow: 'rgba(167,139,250,0.4)', bg: 'from-violet-400/20 to-purple-400/5' },
  surprise:   { emoji: '😲', label: 'Surprise',   color: '#fb923c', glow: 'rgba(251,146,60,0.4)',  bg: 'from-orange-400/20 to-amber-400/5'  },
  disgust:    { emoji: '🤢', label: 'Disgust',    color: '#4ade80', glow: 'rgba(74,222,128,0.4)',  bg: 'from-green-400/20 to-emerald-400/5' },
  anticipation:{ emoji: '🤩', label: 'Anticipation', color: '#f472b6', glow: 'rgba(244,114,182,0.4)', bg: 'from-pink-400/20 to-fuchsia-400/5' },
  trust:      { emoji: '🤝', label: 'Trust',      color: '#2dd4bf', glow: 'rgba(45,212,191,0.4)',  bg: 'from-teal-400/20 to-cyan-400/5'     },
  neutral:    { emoji: '😐', label: 'Neutral',    color: '#94a3b8', glow: 'rgba(148,163,184,0.3)', bg: 'from-slate-400/20 to-gray-400/5'    },
}

const SAMPLE_TEXTS = [
  "I just got promoted at work! This is the best day of my life, I can't stop smiling!",
  "I can't believe they canceled my favorite show. I've been waiting for the finale for months...",
  "The project deadline is tomorrow and I haven't even started. My heart is racing.",
  "I'm not sure what to make of this. It just feels like another ordinary Tuesday.",
  "Ew, I cannot believe someone actually thought this was a good idea. It's revolting.",
  "Wait — she said YES?! Oh my god, I did NOT see that coming!!",
]

// ─── Offline Emotion Detection (No API Key Needed) ────────────────────
async function detectEmotions(text) {
  await new Promise(resolve => setTimeout(resolve, 1500))

  const t = text.toLowerCase()

  // ── Negation check ────────────────────────────────────────────────
  const negations = ["not","no","never","don't","doesn't","didn't","won't","can't","cannot","neither","nor","barely","hardly","nothing"]
  const isNegated = (word) => {
    const idx = t.indexOf(word)
    if (idx === -1) return false
    const before = t.slice(Math.max(0, idx - 30), idx)
    return negations.some(n => before.includes(n + ' '))
  }

  // ── Weighted keyword map (high / medium / low weight tiers) ───────
  const keywordMap = {
    joy: [
      ['overjoyed','ecstatic','thrilled','elated','euphoric','best day','so happy','love it','absolutely love','best day of my life','over the moon','on top of the world'],
      ['happy','excited','wonderful','amazing','fantastic','great news','promoted','passed','won','yay','celebrate','smile','laugh','blessed','grateful','delighted','cheerful','joyful','gleeful'],
      ['good','nice','glad','pleased','fine','enjoy','like','fun','sweet','cool','great']
    ],
    sadness: [
      ['devastated','heartbroken','shattered','sobbing','grief','mourning','lost everything','miss you so much','deeply sad','cried myself','broken heart'],
      ['sad','crying','miss','lonely','depressed','hopeless','miserable','disappointed','hurts','empty','alone','regret','tears','broken','grief','mourning','devastated'],
      ['unfortunate','down','blue','gloomy','low','upset','dull','tired of','unhappy']
    ],
    anger: [
      ['furious','outraged','livid','enraged','infuriated','how dare','absolutely furious','so angry','fed up','blood boils','make me sick','worst person','worst ai','hate you','hate this'],
      ['angry','mad','hate','frustrated','annoyed','irritated','unfair','stupid','ridiculous','unacceptable','betrayed','lied','worst','terrible','pathetic','useless','trash','garbage','horrible','disgusting','rage','fury'],
      ['bothered','dislike','ugh','seriously','come on','why would','bad','poor','wrong','awful']
    ],
    fear: [
      ['terrified','petrified','horrified','paralyzed','dreading','nightmare','so scared','heart racing','panic attack','dread','horror'],
      ['scared','afraid','anxious','nervous','worried','fear','frightened','dread','horror','shaking','trembling','terrifying','phobia','terror'],
      ['uneasy','unsure','hesitant','doubt','concerning','risky','dangerous','threatening']
    ],
    surprise: [
      ['unbelievable','speechless','mind blown','cannot believe','no way','oh my god','what the','totally shocked','did not expect','did not see that coming','blown away'],
      ['shocked','surprised','unexpected','stunned','astonished','amazed','wow','wait what','suddenly','out of nowhere','unreal','floored'],
      ['weird','strange','odd','unusual','interesting','huh','wait','really']
    ],
    disgust: [
      ['revolting','repulsive','nauseating','absolutely disgusting','makes me sick','vile','appalling','sickening','utterly disgusting','feel sick','stomach turn'],
      ['disgusting','gross','horrible','nasty','awful','yuck','ew','repugnant','filthy','hideous','disturbing','worst ever','ever seen','pathetic','repelled','revolted'],
      ['bad','wrong','terrible','unpleasant','off','dirty','foul','yucky']
    ],
    anticipation: [
      ['cannot wait','counting down','so excited for','looking forward','eagerly waiting','buzzing','hyped','can barely sleep','on the edge of my seat'],
      ['excited','waiting','soon','upcoming','hope','planning','ready','prepare','expect','anticipate','eager','countdown','anxious for'],
      ['maybe','perhaps','might','could','wonder','curious','interested','upcoming']
    ],
    trust: [
      ['completely trust','fully confident','absolutely certain','without doubt','guaranteed','proven','100 percent','rely on'],
      ['trust','believe','confident','reliable','honest','faithful','loyal','certain','sure','safe','secure','promise','depend'],
      ['think','seems','probably','likely','okay with','comfortable','assured']
    ],
  }

  // ── Score calculation ─────────────────────────────────────────────
  const scores = { joy:0, sadness:0, anger:0, fear:0, surprise:0, disgust:0, anticipation:0, trust:0, neutral:0 }
  const weights = [35, 20, 8]

  for (const [emotion, tiers] of Object.entries(keywordMap)) {
    for (let tier = 0; tier < tiers.length; tier++) {
      for (const phrase of tiers[tier]) {
        if (t.includes(phrase)) {
          if (!isNegated(phrase)) {
            scores[emotion] += weights[tier]
          } else {
            if (['joy','trust','anticipation'].includes(emotion)) scores.sadness += 10
            else if (['sadness','anger','fear','disgust'].includes(emotion)) scores.joy += 8
          }
        }
      }
    }
  }

  // ── Punctuation & caps boosters ───────────────────────────────────
  const exclamations = (text.match(/!/g) || []).length
  const questions    = (text.match(/\?/g) || []).length
  const capsWords    = (text.match(/\b[A-Z]{2,}\b/g) || []).length

  if (exclamations >= 2) { scores.joy += 10; scores.surprise += 10; scores.anger += 5 }
  else if (exclamations === 1) { scores.joy += 5; scores.surprise += 5 }
  if (questions >= 2) { scores.surprise += 10; scores.fear += 5 }
  if (capsWords >= 2) { scores.anger += 15; scores.surprise += 10 }
  if (text.includes('...')) { scores.sadness += 10; scores.neutral += 5 }

  // ── Find primary emotion ──────────────────────────────────────────
  let primary = 'neutral'
  let maxScore = 0
  for (const [emotion, score] of Object.entries(scores)) {
    if (emotion !== 'neutral' && score > maxScore) {
      maxScore = score
      primary = emotion
    }
  }

  if (maxScore === 0) {
    scores.neutral = 60
    primary = 'neutral'
  } else {
    scores.neutral = Math.max(5, 30 - maxScore)
    for (const k in scores) scores[k] = Math.min(100, scores[k])
  }

  // ── Intensity ─────────────────────────────────────────────────────
  const intensity = maxScore >= 55 ? 'high' : maxScore >= 25 ? 'medium' : 'low'

  // ── Sentiment ─────────────────────────────────────────────────────
  const posScore = scores.joy + scores.anticipation + scores.trust
  const negScore = scores.sadness + scores.anger + scores.fear + scores.disgust
  const sentiment = posScore > negScore + 20 ? 'positive'
                  : negScore > posScore + 20 ? 'negative'
                  : posScore > 10 && negScore > 10 ? 'mixed'
                  : 'neutral'

  // ── Tone & Insight ────────────────────────────────────────────────
  const tones = {
    joy:'euphoric', sadness:'melancholic', anger:'furious',
    fear:'anxious', surprise:'astonished', disgust:'revolted',
    anticipation:'eager', trust:'confident', neutral:'composed'
  }
  const insights = {
    joy:          'Strong positive energy and happiness radiates through the text.',
    sadness:      'Deep emotional pain and sense of loss is clearly expressed.',
    anger:        'Intense frustration and displeasure dominate the message.',
    fear:         'Anxiety and worry are the primary emotional drivers here.',
    surprise:     'Unexpected events have triggered a strong emotional reaction.',
    disgust:      'Strong feelings of repulsion and aversion are expressed.',
    anticipation: 'Excited, forward-looking energy and eagerness are present.',
    trust:        'Confidence, reliability and security are the key feelings.',
    neutral:      'Text is balanced with no dominant emotional signal detected.',
  }

  // ── Keywords ──────────────────────────────────────────────────────
  const allPhrases = keywordMap[primary]?.flat() || []
  const found = allPhrases.filter(w => t.includes(w)).slice(0, 3)
  const kwResult = found.length > 0 ? found : ['expression', 'context', 'language']

  return { primary, scores, intensity, sentiment, tone: tones[primary], insight: insights[primary], keywords: kwResult }
}

// ─── Sub-components ─────────────────────────────────────────────────────

function EmotionOrb({ emotion, intensity }) {
  const cfg = EMOTIONS[emotion] || EMOTIONS.neutral
  const sizes = { low: 120, medium: 150, high: 180 }
  const size = sizes[intensity] || 150

  return (
    <div className="flex items-center justify-center" style={{ height: 220 }}>
      <div
        className="animate-orb-pulse animate-float relative flex items-center justify-center rounded-full"
        style={{
          width: size,
          height: size,
          background: `radial-gradient(circle at 35% 35%, ${cfg.color}cc, ${cfg.color}44)`,
          boxShadow: `0 0 60px ${cfg.glow}, 0 0 120px ${cfg.glow}`,
          border: `2px solid ${cfg.color}66`,
        }}
      >
        <span style={{ fontSize: size * 0.38 }}>{cfg.emoji}</span>
        {/* Ring */}
        <div
          className="absolute inset-0 rounded-full animate-spin-slow"
          style={{
            border: `1px dashed ${cfg.color}44`,
            transform: 'scale(1.25)',
          }}
        />
      </div>
    </div>
  )
}

function ScoreBar({ emotion, score, maxScore, delay }) {
  const cfg = EMOTIONS[emotion]
  const pct = maxScore > 0 ? Math.round((score / maxScore) * 100) : 0

  return (
    <div
      className="animate-fade-up"
      style={{ animationDelay: `${delay}ms`, opacity: 0 }}
    >
      <div className="flex items-center justify-between mb-1">
        <span className="flex items-center gap-2 text-sm" style={{ color: '#c4c0b8' }}>
          <span>{cfg.emoji}</span>
          <span style={{ fontFamily: 'var(--font-body)' }}>{cfg.label}</span>
        </span>
        <span className="text-xs font-semibold" style={{ color: cfg.color }}>{score}</span>
      </div>
      <div className="rounded-full overflow-hidden" style={{ background: 'rgba(255,255,255,0.07)', height: 6 }}>
        <div
          className="emotion-bar"
          style={{
            '--target-width': `${pct}%`,
            background: `linear-gradient(90deg, ${cfg.color}88, ${cfg.color})`,
            width: `${pct}%`,
          }}
        />
      </div>
    </div>
  )
}

function HistoryItem({ item, onClick }) {
  const cfg = EMOTIONS[item.result.primary] || EMOTIONS.neutral
  const preview = item.text.length > 60 ? item.text.slice(0, 60) + '…' : item.text
  return (
    <button
      onClick={() => onClick(item)}
      className="history-item w-full text-left px-4 py-3 rounded-xl flex items-start gap-3"
    >
      <span className="text-xl mt-0.5">{cfg.emoji}</span>
      <div className="flex-1 min-w-0">
        <p className="text-xs truncate" style={{ color: '#8a8680' }}>{preview}</p>
        <p className="text-xs mt-0.5 font-semibold" style={{ color: cfg.color }}>{cfg.label} · {item.result.tone}</p>
      </div>
    </button>
  )
}

// ─── Main App ────────────────────────────────────────────────────────────
export default function App() {
  const [text, setText] = useState('')
  const [result, setResult] = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)
  const [history, setHistory] = useState([])
  const [charCount, setCharCount] = useState(0)
  const textareaRef = useRef(null)

  const maxChars = 500

  const handleTextChange = (e) => {
    const val = e.target.value
    if (val.length <= maxChars) {
      setText(val)
      setCharCount(val.length)
    }
  }

  const handleAnalyze = async () => {
    if (!text.trim() || loading) return
    setLoading(true)
    setError(null)
    setResult(null)
    try {
      const res = await detectEmotions(text.trim())
      setResult(res)
      setHistory(prev => [{ text: text.trim(), result: res, id: Date.now() }, ...prev].slice(0, 10))
    } catch (e) {
      setError('Failed to analyze. Check your API connection and try again.')
    } finally {
      setLoading(false)
    }
  }

  const handleSample = (sample) => {
    setText(sample)
    setCharCount(sample.length)
    setResult(null)
    textareaRef.current?.focus()
  }

  const handleHistoryClick = (item) => {
    setText(item.text)
    setCharCount(item.text.length)
    setResult(item.result)
  }

  const primaryCfg = result ? (EMOTIONS[result.primary] || EMOTIONS.neutral) : null

  const sortedEmotions = result
    ? Object.entries(result.scores).sort(([, a], [, b]) => b - a)
    : []

  const maxScore = sortedEmotions[0]?.[1] || 1

  const sentimentColors = {
    positive: '#4ade80', negative: '#f87171', neutral: '#94a3b8', mixed: '#fb923c'
  }
  const intensityIcons = { low: '○', medium: '◑', high: '●' }

  return (
    <div className="noise min-h-screen" style={{ background: '#0a0a0f' }}>
      {/* Ambient bg blobs */}
      <div className="fixed inset-0 pointer-events-none overflow-hidden">
        <div className="absolute rounded-full blur-3xl opacity-15"
          style={{ width: 600, height: 600, top: -200, left: -200, background: 'radial-gradient(circle, #7c3aed, transparent)' }} />
        <div className="absolute rounded-full blur-3xl opacity-10"
          style={{ width: 500, height: 500, bottom: -150, right: -150, background: 'radial-gradient(circle, #0ea5e9, transparent)' }} />
        {result && primaryCfg && (
          <div className="absolute rounded-full blur-3xl transition-all duration-1000"
            style={{
              width: 700, height: 700, top: '20%', left: '30%',
              transform: 'translate(-50%,-50%)',
              background: `radial-gradient(circle, ${primaryCfg.glow}, transparent)`,
              opacity: 0.2,
            }} />
        )}
      </div>

      <div className="relative z-10 max-w-6xl mx-auto px-6 py-10">

        {/* Header */}
        <header className="mb-10">
          <div className="flex items-center gap-3 mb-2">
            <div className="w-8 h-8 rounded-lg flex items-center justify-center text-base"
              style={{ background: 'linear-gradient(135deg, #7c3aed, #0ea5e9)' }}>
              🧠
            </div>
            <span className="text-xs tracking-widest uppercase font-display" style={{ color: '#6b6760' }}>
              Finding Emotions Through Intelligence
            </span>
          </div>
          <h1 className="font-display text-5xl font-extrabold tracking-tight shimmer-text leading-none mb-3">
            EmoSense
          </h1>
          <p style={{ color: '#6b6760', fontFamily: 'var(--font-body)', fontSize: 15 }}>
            Detect emotions hidden in any text using AI 
          </p>
        </header>

        <div className="grid grid-cols-1 gap-6" style={{ gridTemplateColumns: 'minmax(0,1.2fr) minmax(0,0.8fr)' }}>

          {/* LEFT COLUMN */}
          <div className="flex flex-col gap-5">

            {/* Input Card */}
            <div className="glass-card rounded-2xl p-5">
              <label className="block text-xs tracking-widest uppercase mb-3 font-display" style={{ color: '#6b6760' }}>
                Enter your text
              </label>
              <textarea
                ref={textareaRef}
                value={text}
                onChange={handleTextChange}
                placeholder="Type anything — a tweet, a journal entry, a message, a review... and watch the emotions come alive."
                rows={5}
                className="w-full bg-transparent resize-none text-sm leading-relaxed placeholder-gray-600"
                style={{ color: '#f0eee8', fontFamily: 'var(--font-body)', border: 'none' }}
              />
              <div className="flex items-center justify-between mt-3 pt-3" style={{ borderTop: '1px solid rgba(255,255,255,0.06)' }}>
                <span className="text-xs" style={{ color: charCount > maxChars * 0.9 ? '#f87171' : '#4a4845' }}>
                  {charCount}/{maxChars}
                </span>
                <button
                  onClick={handleAnalyze}
                  disabled={!text.trim() || loading}
                  className="px-6 py-2 rounded-xl text-sm font-semibold font-display transition-all duration-200 disabled:opacity-40 disabled:cursor-not-allowed"
                  style={{
                    background: loading ? 'rgba(255,255,255,0.1)' : 'linear-gradient(135deg, #7c3aed, #0ea5e9)',
                    color: '#fff',
                    boxShadow: loading ? 'none' : '0 4px 24px rgba(124,58,237,0.35)',
                  }}
                >
                  {loading ? (
                    <span className="flex items-center gap-2">
                      <svg className="w-4 h-4 animate-spin-slow" viewBox="0 0 24 24" fill="none">
                        <circle cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="3" strokeDasharray="40" strokeDashoffset="10" />
                      </svg>
                      Analyzing…
                    </span>
                  ) : '✦ Detect Emotions'}
                </button>
              </div>
            </div>

            {/* Sample Texts */}
            <div>
              <p className="text-xs tracking-widest uppercase mb-3 font-display" style={{ color: '#4a4845' }}>
                Try a sample
              </p>
              <div className="flex flex-wrap gap-2">
                {SAMPLE_TEXTS.map((s, i) => (
                  <button
                    key={i}
                    onClick={() => handleSample(s)}
                    className="px-3 py-1.5 rounded-lg text-xs transition-all duration-150"
                    style={{
                      background: 'rgba(255,255,255,0.04)',
                      border: '1px solid rgba(255,255,255,0.08)',
                      color: '#8a8680',
                      fontFamily: 'var(--font-body)',
                    }}
                    onMouseOver={e => e.currentTarget.style.borderColor = 'rgba(255,255,255,0.2)'}
                    onMouseOut={e => e.currentTarget.style.borderColor = 'rgba(255,255,255,0.08)'}
                  >
                    {['😄','😢','😨','😐','🤢','😲'][i]} Sample {i + 1}
                  </button>
                ))}
              </div>
            </div>

            {/* Error */}
            {error && (
              <div className="rounded-xl px-4 py-3 text-sm" style={{ background: 'rgba(248,113,113,0.1)', border: '1px solid rgba(248,113,113,0.25)', color: '#f87171' }}>
                ⚠ {error}
              </div>
            )}

            {/* Result Details */}
            {result && (
              <div className="animate-fade-up glass-card rounded-2xl p-5 flex flex-col gap-5">

                {/* Tags row */}
                <div className="flex flex-wrap gap-2">
                  <span className="px-3 py-1 rounded-full text-xs font-semibold font-display"
                    style={{ background: `${sentimentColors[result.sentiment]}22`, color: sentimentColors[result.sentiment], border: `1px solid ${sentimentColors[result.sentiment]}44` }}>
                    {result.sentiment.toUpperCase()}
                  </span>
                  <span className="px-3 py-1 rounded-full text-xs font-semibold font-display"
                    style={{ background: 'rgba(255,255,255,0.05)', color: '#c4c0b8', border: '1px solid rgba(255,255,255,0.1)' }}>
                    {intensityIcons[result.intensity]} {result.intensity} intensity
                  </span>
                  <span className="px-3 py-1 rounded-full text-xs font-semibold font-display italic"
                    style={{ background: primaryCfg ? `${primaryCfg.color}22` : 'rgba(255,255,255,0.05)', color: primaryCfg?.color || '#c4c0b8', border: `1px solid ${primaryCfg?.color || '#fff'}33` }}>
                    {result.tone}
                  </span>
                </div>

                {/* Insight */}
                <p className="text-sm leading-relaxed" style={{ color: '#c4c0b8', fontFamily: 'var(--font-body)' }}>
                  <span className="font-semibold" style={{ color: '#f0eee8' }}>AI Insight: </span>
                  {result.insight}
                </p>

                {/* Keywords */}
                {result.keywords?.length > 0 && (
                  <div className="flex flex-wrap gap-2">
                    {result.keywords.map((kw, i) => (
                      <span key={i} className="px-2 py-0.5 rounded text-xs"
                        style={{ background: 'rgba(255,255,255,0.05)', color: '#6b6760', fontFamily: 'var(--font-body)' }}>
                        #{kw}
                      </span>
                    ))}
                  </div>
                )}

                {/* Emotion Bars */}
                <div className="flex flex-col gap-3">
                  {sortedEmotions.map(([emotion, score], i) => (
                    <ScoreBar key={emotion} emotion={emotion} score={score} maxScore={maxScore} delay={i * 60} />
                  ))}
                </div>
              </div>
            )}
          </div>

          {/* RIGHT COLUMN */}
          <div className="flex flex-col gap-5">

            {/* Orb / Idle State */}
            <div className="glass-card rounded-2xl p-6 flex flex-col items-center justify-center" style={{ minHeight: 280 }}>
              {result ? (
                <>
                  <EmotionOrb emotion={result.primary} intensity={result.intensity} />
                  <div className="text-center mt-2">
                    <p className="font-display text-2xl font-bold" style={{ color: primaryCfg?.color }}>
                      {primaryCfg?.label}
                    </p>
                    <p className="text-xs mt-1" style={{ color: '#6b6760' }}>Primary emotion detected</p>
                  </div>
                </>
              ) : (
                <div className="flex flex-col items-center gap-4 text-center" style={{ opacity: 0.4 }}>
                  <div className="text-6xl animate-float">🫀</div>
                  <p className="text-sm font-display" style={{ color: '#6b6760' }}>
                    Your emotion orb will appear here
                  </p>
                </div>
              )}
            </div>

            {/* About card */}
            <div className="glass-card rounded-2xl p-5">
              <p className="text-xs tracking-widest uppercase mb-3 font-display" style={{ color: '#4a4845' }}>
                How it works
              </p>
              <div className="flex flex-col gap-3">
                {[
                  ['✦', 'Input', 'Paste any text — a review, tweet, message, or journal entry.'],
                  ['✦', 'Analyze', 'Claude AI parses linguistic cues and context patterns.'],
                  ['✦', 'Visualize', 'Emotions mapped to Plutchik\'s 8-emotion wheel with scores.'],
                ].map(([icon, title, desc]) => (
                  <div key={title} className="flex items-start gap-3">
                    <span className="text-xs mt-0.5" style={{ color: '#7c3aed' }}>{icon}</span>
                    <div>
                      <span className="text-xs font-semibold font-display" style={{ color: '#f0eee8' }}>{title} </span>
                      <span className="text-xs" style={{ color: '#6b6760' }}>{desc}</span>
                    </div>
                  </div>
                ))}
              </div>
            </div>

            {/* History */}
            {history.length > 0 && (
              <div className="glass-card rounded-2xl overflow-hidden">
                <div className="px-4 py-3" style={{ borderBottom: '1px solid rgba(255,255,255,0.06)' }}>
                  <p className="text-xs tracking-widest uppercase font-display" style={{ color: '#4a4845' }}>
                    Recent analyses
                  </p>
                </div>
                <div className="flex flex-col py-1" style={{ maxHeight: 260, overflowY: 'auto' }}>
                  {history.map(item => (
                    <HistoryItem key={item.id} item={item} onClick={handleHistoryClick} />
                  ))}
                </div>
              </div>
            )}
          </div>
        </div>

        {/* Footer */}
        <footer className="mt-12 text-center">
          <p className="text-xs" style={{ color: '#3a3836', fontFamily: 'var(--font-body)' }}>
            EmoSense · Built with React + Vite + Tailwind CSS v4 · Emotion analysis by Claude AI
          </p>
        </footer>
      </div>
    </div>
  )
}
