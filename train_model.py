# ============================================================
#   EmoSense — Naive Bayes Emotion Classifier (Training Code)
#   Model: Multinomial Naive Bayes + TF-IDF Vectorizer
#   Dataset: 400+ labeled emotion sentences (8 emotions)
#   Author: Bhavadharani | B.Tech IT | KPR Institute
# ============================================================

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import pickle
import warnings
warnings.filterwarnings('ignore')

from sklearn.naive_bayes import MultinomialNB
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score, f1_score
from sklearn.pipeline import Pipeline

# ============================================================
# STEP 1 — DATASET (400 samples, 50 per emotion)
# ============================================================

DATA = [

    # ── JOY ──────────────────────────────────────────────────────────
    ("I just got promoted at work! This is the best day of my life!", "joy"),
    ("We won the championship! I am so happy I could cry!", "joy"),
    ("She said yes! I am getting married, I cannot believe it!", "joy"),
    ("I passed all my exams with flying colors, so thrilled!", "joy"),
    ("This is absolutely wonderful, I love everything about today!", "joy"),
    ("My family surprised me with a party, I feel so loved!", "joy"),
    ("I can't stop smiling, everything is going perfectly!", "joy"),
    ("Best vacation ever, I had the time of my life!", "joy"),
    ("I finally got into my dream college, I am thrilled!", "joy"),
    ("The baby took her first steps today, pure happiness!", "joy"),
    ("I got the job offer I was hoping for, so excited!", "joy"),
    ("Today was absolutely perfect, nothing could go wrong!", "joy"),
    ("I am overjoyed, this is the happiest moment of my life!", "joy"),
    ("We got the house! My dream home is finally ours!", "joy"),
    ("My best friend is back in town, I am ecstatic!", "joy"),
    ("I finished my project and it turned out amazing!", "joy"),
    ("We are having a baby! I am the happiest person alive!", "joy"),
    ("I won the competition, all my hard work paid off!", "joy"),
    ("This surprise party is incredible, I feel so special!", "joy"),
    ("My team won the match, we celebrated all night!", "joy"),
    ("I got a scholarship to study abroad, dreams come true!", "joy"),
    ("The concert was phenomenal, I danced all night with joy!", "joy"),
    ("I reunited with my childhood friend after 10 years!", "joy"),
    ("My book finally got published, I am over the moon!", "joy"),
    ("I feel so grateful and blessed for everything in my life!", "joy"),
    ("We crossed 1 million subscribers, this is unreal!", "joy"),
    ("I aced my driving test on the first attempt!", "joy"),
    ("My daughter got into her dream university!", "joy"),
    ("The surprise worked perfectly, she was so happy!", "joy"),
    ("I finally learned to play my favorite song on guitar!", "joy"),
    ("This is the best birthday I have ever had!", "joy"),
    ("I feel so proud of how far I have come!", "joy"),
    ("My startup got funded, all our efforts are paying off!", "joy"),
    ("I laughed so hard today, my stomach hurts!", "joy"),
    ("Everything feels perfect and I am so content right now!", "joy"),
    ("I love this life, I am so incredibly happy today!", "joy"),
    ("My parents are so proud of me, that means everything!", "joy"),
    ("I just finished my marathon, I feel unstoppable!", "joy"),
    ("We got engaged at the Eiffel Tower, magical moment!", "joy"),
    ("I am bursting with happiness and excitement today!", "joy"),
    ("My hard work finally paid off and I feel amazing!", "joy"),
    ("This moment is everything I ever dreamed of!", "joy"),
    ("I feel pure bliss and joy today, nothing can stop me!", "joy"),
    ("My team crushed it and we are all celebrating!", "joy"),
    ("I woke up and realized all my dreams are coming true!", "joy"),
    ("Best news ever received, jumping with joy right now!", "joy"),
    ("I feel like I am on top of the world today!", "joy"),
    ("Happiness is everywhere today and I love every moment!", "joy"),
    ("I am smiling from ear to ear, life is beautiful!", "joy"),
    ("Today reminded me why I love life so much!", "joy"),

    # ── SADNESS ──────────────────────────────────────────────────────
    ("I can't believe he's gone. I miss him so much.", "sadness"),
    ("She left without saying goodbye. My heart is broken.", "sadness"),
    ("I failed again. I don't think I'll ever be good enough.", "sadness"),
    ("Nobody came to my birthday party. I feel so alone.", "sadness"),
    ("I lost my job today. I don't know what to do.", "sadness"),
    ("My dog passed away last night. I am devastated.", "sadness"),
    ("I have been crying all day and I don't even know why.", "sadness"),
    ("Everything I worked for just fell apart.", "sadness"),
    ("I feel so empty and hollow inside.", "sadness"),
    ("They moved away and I will probably never see them again.", "sadness"),
    ("I miss the way things used to be.", "sadness"),
    ("No one understands what I am going through.", "sadness"),
    ("I feel completely hopeless about my future.", "sadness"),
    ("He broke up with me and I feel shattered.", "sadness"),
    ("My grandfather passed away, he meant the world to me.", "sadness"),
    ("I am so lonely even when surrounded by people.", "sadness"),
    ("I lost my best friend and life feels meaningless.", "sadness"),
    ("Nothing I do ever seems to work out for me.", "sadness"),
    ("I am grieving and it feels like it will never end.", "sadness"),
    ("I gave everything and still it was not enough.", "sadness"),
    ("My heart aches every single day without you.", "sadness"),
    ("I just want to cry and not stop.", "sadness"),
    ("I feel abandoned by everyone I ever trusted.", "sadness"),
    ("This loss is too heavy for me to carry.", "sadness"),
    ("I am drowning in grief and sadness right now.", "sadness"),
    ("I thought things would get better but they only got worse.", "sadness"),
    ("My dreams are slipping away and I feel powerless.", "sadness"),
    ("I have never felt this kind of pain before.", "sadness"),
    ("Everything reminds me of what I have lost.", "sadness"),
    ("I am broken and I do not know how to heal.", "sadness"),
    ("The silence in the house since he left is unbearable.", "sadness"),
    ("I feel like I am fading away slowly.", "sadness"),
    ("No matter how hard I try, sadness always finds me.", "sadness"),
    ("I wish I could go back and change everything.", "sadness"),
    ("I cried myself to sleep again last night.", "sadness"),
    ("My world fell apart the day she walked away.", "sadness"),
    ("I miss my old life so much it physically hurts.", "sadness"),
    ("I tried my best but it still was not good enough.", "sadness"),
    ("I feel deeply sad and I cannot shake it off.", "sadness"),
    ("The loneliness is overwhelming and unbearable.", "sadness"),
    ("My tears won't stop and my heart won't heal.", "sadness"),
    ("I lost someone irreplaceable and nothing feels the same.", "sadness"),
    ("I am so disappointed in myself and in life.", "sadness"),
    ("This heartbreak has left me completely hollow.", "sadness"),
    ("I feel like nobody truly cares about me.", "sadness"),
    ("I am stuck in grief and cannot find a way out.", "sadness"),
    ("My sadness is so deep that even smiling feels fake.", "sadness"),
    ("I cry every night thinking about what could have been.", "sadness"),
    ("I have never felt so lost and broken in my life.", "sadness"),
    ("The pain of losing you never really goes away.", "sadness"),

    # ── ANGER ─────────────────────────────────────────────────────────
    ("How dare they lie to my face! I am absolutely furious!", "anger"),
    ("This is completely unacceptable. I am livid right now.", "anger"),
    ("They cheated me out of my money and nobody cares!", "anger"),
    ("I am so sick of being treated like I do not matter!", "anger"),
    ("That was the most disrespectful thing anyone has ever said to me!", "anger"),
    ("I can't believe they would do something so selfish!", "anger"),
    ("They ruined everything with their stupidity!", "anger"),
    ("I am done. I have had enough of this nonsense!", "anger"),
    ("Who gave them the right to speak to me like that?!", "anger"),
    ("This injustice makes my blood boil.", "anger"),
    ("I warned them and they did not listen, now look at this mess!", "anger"),
    ("Every single time, they let me down. I am furious!", "anger"),
    ("You are the worst person I have ever met!", "anger"),
    ("I hate how they always take advantage of me!", "anger"),
    ("This is absolute garbage and a complete waste of my time!", "anger"),
    ("I am outraged by what they did, it is unacceptable!", "anger"),
    ("They betrayed my trust and I will never forgive them!", "anger"),
    ("I am so angry I cannot even think straight right now!", "anger"),
    ("How could they do this to me after everything I did for them?!", "anger"),
    ("I am fed up with being ignored and disrespected!", "anger"),
    ("This is the worst treatment I have ever received!", "anger"),
    ("I am raging inside and I cannot calm down!", "anger"),
    ("They lied to me again and I am absolutely done!", "anger"),
    ("This is pathetic and I am sick and tired of it!", "anger"),
    ("I cannot stand this anymore, I am so angry!", "anger"),
    ("They always blame me for everything, it is so unfair!", "anger"),
    ("I hate this situation and everyone involved in it!", "anger"),
    ("I am furious that they got away with it again!", "anger"),
    ("This is a joke and I am not laughing, I am enraged!", "anger"),
    ("I could scream right now, this is so infuriating!", "anger"),
    ("They made me feel worthless and I am so angry about it!", "anger"),
    ("I am done tolerating this disrespect from everyone!", "anger"),
    ("This is absolutely ridiculous and I am seething!", "anger"),
    ("I feel betrayed, disrespected and completely furious!", "anger"),
    ("I am so mad I could explode right now!", "anger"),
    ("They took everything from me and I hate them for it!", "anger"),
    ("I am not going to stand for this kind of treatment!", "anger"),
    ("This is outrageous and I want justice right now!", "anger"),
    ("I am burning with anger and I need it to stop!", "anger"),
    ("They showed zero respect and I am absolutely livid!", "anger"),
    ("I cannot believe how terrible and unfair this situation is!", "anger"),
    ("This made me so angry that I could not even speak!", "anger"),
    ("I am disgusted by their behavior and I am furious!", "anger"),
    ("They always do this and I am sick of it!", "anger"),
    ("I have never been this angry in my entire life!", "anger"),
    ("This is wrong and I will not stay quiet about it!", "anger"),
    ("I hate everything about this situation, it is so unfair!", "anger"),
    ("They crossed a line and now I am absolutely furious!", "anger"),
    ("I am so enraged by their actions and total disregard!", "anger"),
    ("This is the last straw, I am done with all of it!", "anger"),

    # ── FEAR ──────────────────────────────────────────────────────────
    ("I heard strange noises downstairs and I am home alone.", "fear"),
    ("The doctor found something on the scan. I am terrified.", "fear"),
    ("I have a presentation in front of 500 people tomorrow.", "fear"),
    ("My heart is racing, I feel like something bad is about to happen.", "fear"),
    ("I am scared I will never find my way out of this situation.", "fear"),
    ("The plane started shaking and I could not breathe from fear.", "fear"),
    ("I am afraid to check my bank account after this month.", "fear"),
    ("What if I fail and disappoint everyone who believed in me?", "fear"),
    ("The test results come back tomorrow and I am dreading it.", "fear"),
    ("I keep having nightmares about losing everyone I love.", "fear"),
    ("I am paralyzed with fear, I do not know what to do.", "fear"),
    ("Something feels very wrong and I cannot shake this dread.", "fear"),
    ("I am terrified of what the future holds for me.", "fear"),
    ("I cannot sleep because I am so anxious about tomorrow.", "fear"),
    ("I feel a deep sense of dread that I cannot explain.", "fear"),
    ("I am scared to walk home alone at night.", "fear"),
    ("The thought of failing terrifies me more than anything.", "fear"),
    ("I am so anxious that my hands are shaking right now.", "fear"),
    ("I do not know what is going to happen and it scares me.", "fear"),
    ("I am afraid that no matter what I do it will not be enough.", "fear"),
    ("My worst nightmare might actually be coming true.", "fear"),
    ("I feel so unsafe and frightened right now.", "fear"),
    ("I am dreading the confrontation that is coming.", "fear"),
    ("I cannot stop worrying no matter how hard I try.", "fear"),
    ("The anxiety is so overwhelming that I cannot function.", "fear"),
    ("I am scared of losing the people I love most.", "fear"),
    ("Something terrible might happen and I am helpless.", "fear"),
    ("The fear inside me is so strong I cannot breathe properly.", "fear"),
    ("I am terrified of making the wrong decision.", "fear"),
    ("I keep imagining the worst and I cannot stop myself.", "fear"),
    ("My heart pounds every time I think about it.", "fear"),
    ("I am afraid that everything is about to fall apart.", "fear"),
    ("I feel threatened and unsafe in this environment.", "fear"),
    ("I am so frightened that I want to run away.", "fear"),
    ("The fear of failure haunts me every single day.", "fear"),
    ("I cannot escape this feeling of impending doom.", "fear"),
    ("I am panic-stricken and do not know how to calm down.", "fear"),
    ("I am afraid of being alone forever.", "fear"),
    ("The nightmare felt so real that I woke up screaming.", "fear"),
    ("I am too scared to even try because of what might happen.", "fear"),
    ("My anxiety is at an all-time high and I am struggling.", "fear"),
    ("I am terrified of being rejected again.", "fear"),
    ("What if something horrible happens and I cannot stop it?", "fear"),
    ("I feel constant fear and it is ruining my life.", "fear"),
    ("I am scared of the dark ever since that night.", "fear"),
    ("The thought of what could go wrong keeps me up at night.", "fear"),
    ("I am afraid that I will never be truly safe again.", "fear"),
    ("My fear is irrational but I cannot control it.", "fear"),
    ("I am dreading every single day that passes.", "fear"),
    ("I cannot shake this overwhelming sense of terror.", "fear"),

    # ── SURPRISE ──────────────────────────────────────────────────────
    ("Wait she actually did it?! I did NOT see that coming!", "surprise"),
    ("I opened the door and everyone yelled surprise! I was speechless.", "surprise"),
    ("He quit his job at Google to become a farmer?! What?!", "surprise"),
    ("I can't believe it, I won the lottery?!", "surprise"),
    ("Out of nowhere, my old friend called after 10 years!", "surprise"),
    ("They announced the sequel and the entire internet exploded!", "surprise"),
    ("She revealed she had been learning my language in secret!", "surprise"),
    ("The plot twist at the end completely floored me!", "surprise"),
    ("I did not expect that at all, I am still in shock!", "surprise"),
    ("Oh my gosh, is that really you?! I had no idea!", "surprise"),
    ("The ending came out of nowhere, I am still processing it.", "surprise"),
    ("He proposed in the middle of the restaurant, I was stunned!", "surprise"),
    ("I cannot believe this actually happened, it is unreal!", "surprise"),
    ("This is the most unexpected thing that has ever happened to me!", "surprise"),
    ("I am completely blown away by this news!", "surprise"),
    ("Nobody told me about this, I am absolutely shocked!", "surprise"),
    ("This came out of nowhere and I am speechless!", "surprise"),
    ("I never would have guessed this in a million years!", "surprise"),
    ("The surprise party was so unexpected, I nearly fainted!", "surprise"),
    ("What?! That cannot be true, I am totally astonished!", "surprise"),
    ("I am still in disbelief, I cannot process this!", "surprise"),
    ("They showed up at my door unannounced and I was stunned!", "surprise"),
    ("This revelation has completely changed everything I thought I knew!", "surprise"),
    ("I had no idea this was happening, I am floored!", "surprise"),
    ("The unexpected news left me completely dumbfounded!", "surprise"),
    ("I was not prepared for this at all, so shocked!", "surprise"),
    ("This completely blindsided me and I am still reeling!", "surprise"),
    ("I cannot believe they kept this secret for so long!", "surprise"),
    ("The twist was so shocking I had to reread it three times!", "surprise"),
    ("Oh wow I genuinely did not see any of that coming!", "surprise"),
    ("This is beyond anything I could have ever imagined!", "surprise"),
    ("I am still in shock and cannot stop talking about it!", "surprise"),
    ("The announcement caught everyone completely off guard!", "surprise"),
    ("I dropped everything when I heard the unexpected news!", "surprise"),
    ("I am astonished by this sudden and unexpected turn of events!", "surprise"),
    ("Nobody expected this outcome and we are all stunned!", "surprise"),
    ("The surprise was so overwhelming I burst into tears!", "surprise"),
    ("I was completely caught off guard by what happened!", "surprise"),
    ("This unexpected development has left me absolutely amazed!", "surprise"),
    ("I had no clue and now I cannot believe it!", "surprise"),
    ("This is so random and unexpected, I am shocked!", "surprise"),
    ("They did what?! I cannot believe it, totally surprised!", "surprise"),
    ("The completely unexpected result shocked everyone present!", "surprise"),
    ("I am genuinely surprised and do not know what to say!", "surprise"),
    ("This came as a total shock to everyone including me!", "surprise"),
    ("I am overwhelmed with surprise and cannot stop blinking!", "surprise"),
    ("Never in my life did I expect something like this!", "surprise"),
    ("This is so unbelievable, I keep pinching myself!", "surprise"),
    ("I was left completely speechless by what just happened!", "surprise"),
    ("This shocking news has turned my whole world upside down!", "surprise"),

    # ── DISGUST ───────────────────────────────────────────────────────
    ("That food smelled absolutely revolting, I nearly gagged.", "disgust"),
    ("I cannot believe someone actually did that, it is sickening.", "disgust"),
    ("The corruption in this system makes me feel physically ill.", "disgust"),
    ("Ew, that is the most repulsive thing I have ever seen.", "disgust"),
    ("How can anyone treat animals that way? It is disgusting.", "disgust"),
    ("The way he spoke to the staff was absolutely nauseating.", "disgust"),
    ("I feel gross just thinking about what they did.", "disgust"),
    ("That video was so disturbing I had to look away.", "disgust"),
    ("What a vile and disgusting display of behavior.", "disgust"),
    ("I would never touch that, it is utterly repugnant.", "disgust"),
    ("The smell was so awful I had to leave the room.", "disgust"),
    ("I am appalled by how disgusting this situation is.", "disgust"),
    ("You are the worst AI I have ever seen, absolutely terrible.", "disgust"),
    ("That is absolutely gross and I want nothing to do with it.", "disgust"),
    ("I cannot stand the sight of this, it makes me sick.", "disgust"),
    ("This is the most repulsive behavior I have witnessed.", "disgust"),
    ("I feel nauseated just looking at this disgusting mess.", "disgust"),
    ("This is so vile and horrible, I cannot look at it.", "disgust"),
    ("That was absolutely disgusting behavior and I am appalled.", "disgust"),
    ("I have never seen anything so revolting in my life.", "disgust"),
    ("This makes my stomach turn, it is so disgusting!", "disgust"),
    ("I am deeply disgusted by what I just witnessed.", "disgust"),
    ("That is just plain gross and totally unacceptable.", "disgust"),
    ("I cannot believe people actually behave in such a vile way.", "disgust"),
    ("This is nauseating and I want to get as far away as possible.", "disgust"),
    ("I feel sick to my stomach because of what I just saw.", "disgust"),
    ("That is the most disgusting thing I have ever encountered.", "disgust"),
    ("I am thoroughly disgusted by this repulsive situation.", "disgust"),
    ("This is absolutely filthy and disgusting beyond words.", "disgust"),
    ("The horrible smell made me feel completely nauseous.", "disgust"),
    ("I cannot stomach this, it is too revolting for me.", "disgust"),
    ("That behavior was reprehensible and utterly disgusting.", "disgust"),
    ("I am revolted by what I just experienced, so gross!", "disgust"),
    ("The worst thing I have ever tasted in my entire life.", "disgust"),
    ("This is beyond gross and I feel disgusted to my core.", "disgust"),
    ("I walked in on something so disgusting I wanted to scream.", "disgust"),
    ("I am so disgusted that I cannot even find the right words.", "disgust"),
    ("That is absolutely hideous and I refuse to accept it.", "disgust"),
    ("I cannot handle how disgusting this whole thing is.", "disgust"),
    ("The whole scene was repulsive and made me want to leave.", "disgust"),
    ("I am completely revolted by this garbage behavior.", "disgust"),
    ("This rubbish is disgusting and I want nothing to do with it.", "disgust"),
    ("I have never felt so repelled by anything in my life.", "disgust"),
    ("That is trash behavior and I am disgusted by it.", "disgust"),
    ("I am sickened and appalled by this revolting situation.", "disgust"),
    ("Everything about this is disgusting, gross and vile.", "disgust"),
    ("I feel physically ill after what I just witnessed.", "disgust"),
    ("That is pathetic and disgusting and I have lost all respect.", "disgust"),
    ("This is so nasty that I cannot look at it anymore.", "disgust"),
    ("I am utterly and completely disgusted by all of this.", "disgust"),

    # ── ANTICIPATION ──────────────────────────────────────────────────
    ("I cannot wait for tomorrow, I have been counting down the days!", "anticipation"),
    ("The trip is finally happening next week, I am buzzing!", "anticipation"),
    ("Results drop at midnight and I can barely contain myself.", "anticipation"),
    ("I have been preparing for this moment my entire life.", "anticipation"),
    ("Every day brings me closer to my goal, I am so eager!", "anticipation"),
    ("The trailer gave me goosebumps, I need to see this movie!", "anticipation"),
    ("She is coming to visit next month and I am already excited!", "anticipation"),
    ("I submitted my application and now I wait in hopeful suspense.", "anticipation"),
    ("The product launches tomorrow and I have been hyped for weeks!", "anticipation"),
    ("I keep imagining how amazing it is going to be.", "anticipation"),
    ("Only 3 more days until the concert, I cannot wait!", "anticipation"),
    ("The anticipation is killing me, I need to know what happens next!", "anticipation"),
    ("I am so ready for this new chapter in my life to begin!", "anticipation"),
    ("I have been looking forward to this for months!", "anticipation"),
    ("I can feel that something amazing is just around the corner!", "anticipation"),
    ("The wait is almost over and I am bursting with excitement!", "anticipation"),
    ("I have everything planned and I cannot wait to start!", "anticipation"),
    ("This upcoming event is going to be absolutely incredible!", "anticipation"),
    ("I am eagerly counting down to the big day!", "anticipation"),
    ("I have been waiting for this opportunity for years!", "anticipation"),
    ("The possibilities ahead are so exciting I can barely sleep!", "anticipation"),
    ("I am on the edge of my seat waiting for the announcement!", "anticipation"),
    ("I have been dreaming about this moment for so long!", "anticipation"),
    ("I am so pumped up and ready for what is coming!", "anticipation"),
    ("Tomorrow cannot come soon enough, I am so eager!", "anticipation"),
    ("The countdown to the big day has officially begun!", "anticipation"),
    ("I cannot stop thinking about the exciting thing ahead!", "anticipation"),
    ("I am overflowing with anticipation and positive energy!", "anticipation"),
    ("Everything is set and I am ready and raring to go!", "anticipation"),
    ("I wake up every morning excited about what is coming!", "anticipation"),
    ("I have been preparing for this and the time is almost here!", "anticipation"),
    ("I am so thrilled and hopeful about what lies ahead!", "anticipation"),
    ("The big moment is approaching and I am full of excitement!", "anticipation"),
    ("I have been planning for this for ages and it is almost time!", "anticipation"),
    ("I feel a wonderful sense of excitement about the future!", "anticipation"),
    ("I am brimming with hope and excitement about what is next!", "anticipation"),
    ("I keep checking the clock, I cannot wait any longer!", "anticipation"),
    ("I am ready to take on everything that is coming my way!", "anticipation"),
    ("This is going to be the best experience of my life!", "anticipation"),
    ("The future looks so bright and I am excited to embrace it!", "anticipation"),
    ("I am fully prepared and eagerly waiting for this to begin!", "anticipation"),
    ("I have a wonderful feeling that great things are coming!", "anticipation"),
    ("I am anxiously and excitedly awaiting the big reveal!", "anticipation"),
    ("Something great is on the horizon and I can feel it!", "anticipation"),
    ("I cannot wait to see what amazing things the future holds!", "anticipation"),
    ("The excitement is building and I am loving every moment!", "anticipation"),
    ("I am so hopeful and expectant about everything ahead!", "anticipation"),
    ("I have butterflies from how excited I am for what is coming!", "anticipation"),
    ("This is going to be incredible and I am fully ready!", "anticipation"),
    ("I can feel the momentum building towards something great!", "anticipation"),

    # ── NEUTRAL ───────────────────────────────────────────────────────
    ("I went to the store and bought some groceries.", "neutral"),
    ("The meeting is scheduled for 3 PM on Tuesday.", "neutral"),
    ("She sent me the document via email this morning.", "neutral"),
    ("The temperature today is around 25 degrees Celsius.", "neutral"),
    ("I read the report and noted the key findings.", "neutral"),
    ("The bus arrives at the station every 20 minutes.", "neutral"),
    ("He completed the assignment and submitted it on time.", "neutral"),
    ("The package was delivered to the front door.", "neutral"),
    ("I updated the software to the latest version.", "neutral"),
    ("The class starts at 9 AM every Monday.", "neutral"),
    ("She lives in the apartment on the third floor.", "neutral"),
    ("The conference will be held in Chennai this year.", "neutral"),
    ("I made a cup of tea and sat down to read.", "neutral"),
    ("The report needs to be submitted by Friday.", "neutral"),
    ("He parked the car in the basement.", "neutral"),
    ("The library closes at 8 PM on weekdays.", "neutral"),
    ("I called the office to reschedule my appointment.", "neutral"),
    ("The train was delayed by 15 minutes today.", "neutral"),
    ("She bought a new notebook for her classes.", "neutral"),
    ("The weather forecast says it will rain tomorrow.", "neutral"),
    ("I printed the documents before the meeting.", "neutral"),
    ("The project deadline is next Wednesday.", "neutral"),
    ("He ordered food from the restaurant nearby.", "neutral"),
    ("I took notes during the lecture.", "neutral"),
    ("The school reopens after the holidays on Monday.", "neutral"),
    ("I charged my phone before going to bed.", "neutral"),
    ("The office is located on the fifth floor.", "neutral"),
    ("She returned the book to the library.", "neutral"),
    ("I checked the schedule and the event is at noon.", "neutral"),
    ("The program runs for approximately two hours.", "neutral"),
    ("I set the alarm for 6 AM tomorrow.", "neutral"),
    ("He forwarded the email to the relevant team.", "neutral"),
    ("The water bill is due at the end of the month.", "neutral"),
    ("I cleaned the room and organized my desk.", "neutral"),
    ("She submitted the form before the deadline.", "neutral"),
    ("The car needs an oil change next week.", "neutral"),
    ("I added the task to my to-do list.", "neutral"),
    ("He attended the seminar on data science today.", "neutral"),
    ("The restaurant opens at 11 AM on weekdays.", "neutral"),
    ("I downloaded the app and created an account.", "neutral"),
    ("The assignment was straightforward and took one hour.", "neutral"),
    ("She noted the key points from the presentation.", "neutral"),
    ("I confirmed the booking via email.", "neutral"),
    ("He picked up the kids from school at 3 PM.", "neutral"),
    ("The supermarket is a 10-minute walk from here.", "neutral"),
    ("I reviewed the contract before signing it.", "neutral"),
    ("The seminar registration closes on Friday.", "neutral"),
    ("She took the afternoon off to run errands.", "neutral"),
    ("I updated my resume and saved it as a PDF.", "neutral"),
    ("The meeting ran for about 45 minutes in total.", "neutral"),
]


# ============================================================
# STEP 2 — PREPARE DATA
# ============================================================

print("=" * 60)
print("   EmoSense — Naive Bayes Emotion Classifier")
print("=" * 60)

df = pd.DataFrame(DATA, columns=["text", "emotion"])

print(f"\n📊 Dataset Overview:")
print(f"   Total samples  : {len(df)}")
print(f"   Emotions       : {df['emotion'].nunique()}")
print(f"\n   Samples per emotion:")
for emotion, count in df['emotion'].value_counts().items():
    bar = "█" * count
    print(f"   {emotion:<14} {bar} ({count})")


# ============================================================
# STEP 3 — TRAIN / TEST SPLIT
# ============================================================

X = df['text']
y = df['emotion']

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

print(f"\n📂 Train/Test Split:")
print(f"   Training samples : {len(X_train)}")
print(f"   Testing samples  : {len(X_test)}")


# ============================================================
# STEP 4 — BUILD PIPELINE
# ============================================================

pipeline = Pipeline([
    ('tfidf', TfidfVectorizer(
        ngram_range=(1, 2),
        max_features=8000,
        sublinear_tf=True,
        stop_words='english',
        min_df=1,
    )),
    ('nb', MultinomialNB(alpha=0.3))
])

print("\n🔧 Model Architecture:")
print("   TF-IDF Vectorizer  →  Multinomial Naive Bayes")
print("   Ngrams: (1,2) | Max features: 8000 | Alpha: 0.3")


# ============================================================
# STEP 5 — TRAIN
# ============================================================

print("\n⚙️  Training model...")
pipeline.fit(X_train, y_train)
print("   ✓ Training complete!")


# ============================================================
# STEP 6 — EVALUATE
# ============================================================

y_pred = pipeline.predict(X_test)

accuracy = accuracy_score(y_test, y_pred)
f1 = f1_score(y_test, y_pred, average='weighted')

print(f"\n📈 Evaluation Results:")
print(f"   Accuracy  : {accuracy * 100:.1f}%")
print(f"   F1 Score  : {f1 * 100:.1f}%  (weighted)")

cv_scores = cross_val_score(pipeline, X, y, cv=5, scoring='accuracy')
print(f"   CV Accuracy (5-fold): {cv_scores.mean()*100:.1f}% ± {cv_scores.std()*100:.1f}%")

print(f"\n📋 Classification Report:")
print(classification_report(y_test, y_pred, zero_division=0))


# ============================================================
# STEP 7 — PLOTS
# ============================================================

labels = sorted(df['emotion'].unique())
cm = confusion_matrix(y_test, y_pred, labels=labels)

fig, axes = plt.subplots(1, 2, figsize=(18, 7))
fig.suptitle("EmoSense — Naive Bayes Emotion Classifier Results", fontsize=14, fontweight='bold')

sns.heatmap(cm, annot=True, fmt='d', cmap='YlOrRd',
    xticklabels=labels, yticklabels=labels,
    ax=axes[0], linewidths=0.5, linecolor='#eee')
axes[0].set_title("Confusion Matrix", fontweight='bold')
axes[0].set_xlabel("Predicted Label")
axes[0].set_ylabel("True Label")
axes[0].tick_params(axis='x', rotation=45)
axes[0].tick_params(axis='y', rotation=0)

report = classification_report(y_test, y_pred, output_dict=True, zero_division=0)
emotions_in_report = [e for e in labels if e in report]
f1_scores = [report[e]['f1-score'] for e in emotions_in_report]
colors = ['#e74c3c','#3498db','#e67e22','#9b59b6','#f1c40f','#1abc9c','#e91e63','#607d8b']

bars = axes[1].barh(emotions_in_report, f1_scores, color=colors[:len(emotions_in_report)], edgecolor='white')
axes[1].set_xlim(0, 1.15)
axes[1].set_title("Per-Emotion F1 Score", fontweight='bold')
axes[1].set_xlabel("F1 Score")
for bar, score in zip(bars, f1_scores):
    axes[1].text(bar.get_width() + 0.02, bar.get_y() + bar.get_height()/2,
                 f'{score:.2f}', va='center', fontsize=9)

plt.tight_layout()
plt.savefig("emotion_classifier_results.png", dpi=150, bbox_inches='tight')
print("\n📊 Chart saved as: emotion_classifier_results.png")


# ============================================================
# STEP 8 — SAVE MODEL
# ============================================================

with open("emotion_model.pkl", "wb") as f:
    pickle.dump(pipeline, f)

print("💾 Model saved as: emotion_model.pkl")


# ============================================================
# STEP 9 — LIVE PREDICTION DEMO
# ============================================================

def predict_emotion(text):
    prediction = pipeline.predict([text])[0]
    probabilities = pipeline.predict_proba([text])[0]
    classes = pipeline.classes_
    prob_dict = dict(zip(classes, probabilities))
    top3 = sorted(prob_dict.items(), key=lambda x: x[1], reverse=True)[:3]
    return prediction, top3

print("\n" + "=" * 60)
print("   🎯 Live Prediction Demo")
print("=" * 60)

test_sentences = [
    "I just got promoted, this is the best day of my life!",
    "I miss my grandmother so much, it hurts deeply.",
    "How dare they treat people like that, I am furious!",
    "The exam is tomorrow and I am terrified.",
    "Wait she actually won?! I am shocked!",
    "That was absolutely revolting, I feel sick.",
    "I cannot wait for the concert next week!",
    "The meeting starts at 10 AM on Friday.",
    "You are the worst AI I have ever seen!",
    "I am not happy with this result at all.",
    "She smiled and everything felt okay again.",
    "I dread waking up every single morning.",
]

for sentence in test_sentences:
    emotion, top3 = predict_emotion(sentence)
    top3_str = " | ".join([f"{e}: {p*100:.0f}%" for e, p in top3])
    print(f"\n  📝 \"{sentence[:60]}\"")
    print(f"     → Predicted : {emotion.upper()}")
    print(f"     → Top 3     : {top3_str}")


# ============================================================
# STEP 10 — HOW TO LOAD AND USE
# ============================================================

print("\n" + "=" * 60)
print("   📦 How to use the saved model")
print("=" * 60)
print("""
  import pickle

  with open('emotion_model.pkl', 'rb') as f:
      model = pickle.load(f)

  text = "I am so happy today!"
  emotion = model.predict([text])[0]
  print(emotion)  # joy
""")

print("=" * 60)
print("   ✅ Done! Files generated:")
print("      • emotion_model.pkl")
print("      • emotion_classifier_results.png")
print("=" * 60)
