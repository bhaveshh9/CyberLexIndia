# 🛡️ CyberLex India — Cyber Law Awareness Platform

A full-stack web application to educate users about Indian Cyber Laws, built with **Flask + SQLite + modern HTML/CSS/JS**.

## 🚀 Quick Start

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Run the App
```bash
python app.py
```

### 3. Open in Browser
```
http://localhost:5000
```

---

## 📁 Project Structure

```
cyber_law_platform/
├── app.py                    # Main Flask application
├── database.db               # SQLite database (auto-created)
├── requirements.txt          # Python dependencies
├── templates/
│   ├── base.html             # Base template with navbar/footer
│   ├── index.html            # Homepage
│   ├── laws.html             # Laws listing page
│   ├── law_detail.html       # Individual law detail page
│   ├── quiz.html             # Quiz page
│   └── feedback.html        # Feedback form page
└── static/
    ├── css/
    │   └── style.css         # Main stylesheet
    └── js/
        └── main.js           # Main JavaScript
```

---

## ✨ Features

| Feature | Status |
|---------|--------|
| 📜 13 Indian Cyber Laws | ✅ |
| 🔍 Search functionality | ✅ |
| 🌍 Multilingual (EN, HI, MR) | ✅ |
| 🔊 Text-to-Speech audio | ✅ (requires gTTS) |
| ⭐ 15-question MCQ Quiz | ✅ |
| 💬 Feedback system | ✅ |
| 🌙 Dark/Light mode toggle | ✅ |
| 📱 Mobile responsive | ✅ |

---

## 🌍 Languages
- **English** (default)
- **Hindi** (हिंदी) — via googletrans
- **Marathi** (मराठी) — via googletrans

> **Note**: Translation requires `googletrans==4.0.0rc1`. Install with:
> ```bash
> pip install googletrans==4.0.0rc1
> ```

## 🔊 Text-to-Speech
Audio is generated using `gTTS` (Google Text-to-Speech). Requires internet connection.

---

## 📚 Laws Covered

1. IT Act 2000 — Overview
2. Section 43 — Unauthorized Access
3. Section 65 — Tampering with Source Documents
4. Section 66 — Computer-Related Offences (Hacking)
5. Section 66B — Receiving Stolen Computer Resource
6. Section 66C — Identity Theft
7. Section 66D — Cheating by Personation (Online Fraud)
8. Section 66E — Privacy Violation
9. Section 66F — Cyber Terrorism
10. Section 67 — Publishing Obscene Content
11. Section 67A — Sexually Explicit Content
12. Section 67B — Child Pornography (CSAM)
13. Section 72 — Breach of Confidentiality

---

## 🆘 Cybercrime Helpline
**1930** | [cybercrime.gov.in](https://cybercrime.gov.in)

---

## ⚠️ Disclaimer
This platform is for **educational purposes only** and does not constitute legal advice. For legal matters, consult a qualified cyber law attorney.
