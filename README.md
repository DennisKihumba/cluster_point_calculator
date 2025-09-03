Project Overview: KCSE Career Guidance Platform
Goal: Help Form 4 graduates instantly discover courses and universities they qualify for based on their KCSE results—before KUCCPS opens its portal.

🧩 Core Features
1. User Account System
Tech: Flask + MySQL

Functionality:

Secure registration/login (email + password)

Persistent user data (grades, preferences, saved courses)

Future login restores progress

2. KCSE Result Input + Cluster Point Calculator
Tech: Python backend

Logic:

Accept KCSE grades for 4 cluster subjects

Use KUCCPS formula: $$w = \sqrt{\left(\frac{r}{m} \cdot \frac{api}{spi}\right)} \cdot 48$$ (You’ll need to define r, m, api, spi based on subject weights and performance indices)

Data Source: Use KUCCPS 2025/2026 cluster points and cutoff data or Tuko’s breakdown

3. Course & University Matching
Tech: Python + MySQL

Functionality:

Compare calculated cluster points against stored cutoff data

Return list of eligible courses + universities

Filter by interest (e.g., STEM, Business, Arts)

4. AI Career Guidance (Hugging Face)
Tech: Hugging Face API + JS frontend

Functionality:

Candidate can ask: “What careers fit my grades and interests?”

AI suggests paths based on input (grades, interests, goals)

Use models like bert-base-uncased or fine-tuned career guidance models

5. Monetization via InstaSend
Tech: InstaSend API

Functionality:

Charge for premium features (e.g., detailed career reports, mentorship sessions)

Integrate mobile money payments (M-Pesa, Airtel Money)

Track transactions per user

Tech Stack Summary
Layer	Tools Used
Frontend	HTML, CSS, JavaScript
Backend	Python (Flask), MySQL
AI Guidance	Hugging Face API
Auth & Data	Flask-Login, SQLAlchemy
Payments	InstaSend API
Hosting	Render, Railway, or Heroku
🔐 Privacy & Persistence
Use hashed passwords (Flask-Bcrypt)

Store user sessions securely

Backup user data regularly

Optionally allow users to download their career report

🚀 Bonus Features (if time allows)
Progress Tracker: Show how far they’ve explored

Mentorship Portal: Connect with real professionals

Course Popularity Stats: Based on past KUCCPS data

Mobile-first Design: For accessibility on low-end device
