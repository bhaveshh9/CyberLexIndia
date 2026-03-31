"""
Cyber Law Awareness Platform
A Flask-based web application to educate users about Indian Cyber Laws
"""

from flask import Flask, render_template, request, jsonify, send_file
import sqlite3
import os
import io
import json
import requests
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

# ─── Database Setup ───────────────────────────────────────────────────────────

def get_db():
    """Create a database connection."""
    db = sqlite3.connect('database.db')
    db.row_factory = sqlite3.Row
    return db

def init_db():
    """Initialize the database with schema and seed data."""
    db = get_db()
    
    # Create tables
    db.executescript('''
        CREATE TABLE IF NOT EXISTS laws (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            slug TEXT UNIQUE NOT NULL,
            title TEXT NOT NULL,
            section TEXT NOT NULL,
            description TEXT NOT NULL,
            example TEXT NOT NULL,
            punishment TEXT NOT NULL,
            category TEXT NOT NULL
        );

        CREATE TABLE IF NOT EXISTS feedback (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            message TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    ''')

    # Seed laws data if empty
    count = db.execute('SELECT COUNT(*) FROM laws').fetchone()[0]
    if count == 0:
        laws_data = [
            (
                'it-act-2000',
                'Information Technology Act, 2000',
                'Overview',
                'The IT Act 2000 is the primary law in India governing cybercrime and electronic commerce. It provides legal recognition for electronic documents and digital signatures. It was amended in 2008 to address newer forms of cyber offenses. The Act covers a wide range of digital activities including online contracts, electronic records, and cyber offenses. It empowers law enforcement to tackle cybercrime and protects individuals and organizations from digital threats.',
                'A company accepts contracts via email — the IT Act gives these digital agreements the same legal standing as paper contracts. When a bank processes your online transaction, it is protected and regulated under this Act.',
                'Varies by section — individual sections specify penalties ranging from fines to imprisonment up to life in cases of cyber terrorism.',
                'Overview'
            ),
            (
                'section-43',
                'Unauthorized Access to Computer Resources',
                'Section 43',
                'Section 43 deals with unauthorized access to computer systems, networks, or data. It covers acts like accessing without permission, downloading/extracting data, introducing viruses, damaging computer systems, or denying authorized access. This section applies to both intentional and negligent acts. It is a civil liability section, meaning the offender must pay compensation to the victim.',
                'A disgruntled ex-employee logs into their former company\'s server using old credentials and downloads confidential client data. Even if they do not misuse it, merely accessing it without authorization is a violation of Section 43.',
                'Compensation up to ₹1 Crore (civil liability) payable to the affected person. No criminal imprisonment under this section alone.',
                'Access & Privacy'
            ),
            (
                'section-65',
                'Tampering with Computer Source Documents',
                'Section 65',
                'Section 65 makes it illegal to knowingly or intentionally conceal, destroy, or alter any computer source code. Computer source code includes programs, computer commands, design, and layout. This includes software code, website code, and any digital document that is required to be kept or maintained. The offense applies to anyone who alters such code without authorization.',
                'A software developer, before leaving a company, alters the company\'s proprietary source code to introduce bugs or deletes critical files to sabotage the product. This act of tampering is a direct violation of Section 65.',
                'Imprisonment up to 3 years, or fine up to ₹2 Lakhs, or both.',
                'Data & Documents'
            ),
            (
                'section-66',
                'Computer-Related Offences (Hacking)',
                'Section 66',
                'Section 66 covers dishonest or fraudulent acts defined under Section 43. It adds criminal liability to what Section 43 defines as civil wrongs. This includes hacking into systems, spreading viruses, unauthorized data theft, and any act that causes wrongful gain or loss using a computer. The intent to cause damage or gain dishonestly is key to this section.',
                'A hacker breaks into an e-commerce website\'s database, steals thousands of customer credit card details, and sells them on the dark web. This is a classic Section 66 hacking offense involving unauthorized access with fraudulent intent.',
                'Imprisonment up to 3 years, or fine up to ₹5 Lakhs, or both.',
                'Hacking & Fraud'
            ),
            (
                'section-66b',
                'Receiving Stolen Computer Resource',
                'Section 66B',
                'Section 66B targets people who knowingly or dishonestly receive or retain any stolen computer resource or communication device. It is not just the thief who is liable — anyone who knowingly uses stolen data or devices is equally guilty under this section. This provision covers bought, received, or found stolen digital assets.',
                'Someone buys a stolen laptop at a very low price from a street market, knowing it was stolen. They use it for personal work. Both the seller (who stole) and the buyer (who knew it was stolen) are liable under Section 66B.',
                'Imprisonment up to 3 years, or fine up to ₹1 Lakh, or both.',
                'Digital Theft'
            ),
            (
                'section-66c',
                'Identity Theft',
                'Section 66C',
                'Section 66C specifically deals with identity theft in the digital world. It makes it illegal to fraudulently or dishonestly use another person\'s electronic signature, password, or any unique identification feature. This covers using someone\'s login credentials, biometric data, digital certificates, or OTPs to impersonate them online.',
                'A fraudster obtains a victim\'s Aadhaar number and uses it to create a fake digital identity, applies for loans online in the victim\'s name, and disappears with the money. Using someone\'s personal identification details without consent is identity theft under Section 66C.',
                'Imprisonment up to 3 years, and fine up to ₹1 Lakh.',
                'Identity & Privacy'
            ),
            (
                'section-66d',
                'Cheating by Personation Using Computer',
                'Section 66D',
                'Section 66D covers cheating by impersonating someone else using a computer resource or communication device. This includes creating fake online profiles, impersonating companies or government officials to deceive people, and online scams where fraudsters pretend to be someone trustworthy to cheat victims financially.',
                'A fraudster creates a fake website of a popular bank, sends phishing emails to customers asking them to "verify" their account, and collects login credentials. Alternatively, someone pretends to be a government official on social media to extort money — both are classic Section 66D offenses.',
                'Imprisonment up to 3 years, and fine up to ₹1 Lakh.',
                'Online Fraud'
            ),
            (
                'section-66e',
                'Privacy Violation',
                'Section 66E',
                'Section 66E protects individuals from intentional capture, publishing, or transmission of images of a private area of any person without their consent. It covers acts done under circumstances violating the privacy of that person. This section specifically targets voyeurism, non-consensual recording in private spaces, and unauthorized sharing of intimate images.',
                'A person secretly installs a hidden camera in a changing room or bathroom and records videos of people. Sharing someone\'s intimate photos or videos without their consent (revenge porn) also falls under this section — a deeply violating crime addressed by 66E.',
                'Imprisonment up to 3 years, and fine up to ₹2 Lakhs, or both.',
                'Privacy'
            ),
            (
                'section-66f',
                'Cyber Terrorism',
                'Section 66F',
                'Section 66F is one of the most serious provisions in the IT Act. It covers acts of cyber terrorism — attacks on critical infrastructure like power grids, financial systems, or government networks with intent to threaten the unity, integrity, sovereignty, or security of India. It also covers unauthorized access to restricted government computers or those related to national security.',
                'A foreign-backed group of hackers attempts to shut down India\'s power grid by attacking SCADA systems, or a terrorist group tries to access classified defense information by hacking military servers. These constitute cyber terrorism under Section 66F.',
                'Imprisonment up to life imprisonment.',
                'National Security'
            ),
            (
                'section-67',
                'Publishing Obscene Content Online',
                'Section 67',
                'Section 67 prohibits publishing or transmitting any material in electronic form that is lascivious or appeals to the prurient interest, or if its effect tends to deprave and corrupt persons who read, see, or hear it. This essentially criminalizes online obscenity and pornographic content distributed without appropriate restrictions.',
                'A person creates a website hosting and distributing obscene videos and images to the general public without any age verification or restriction. Similarly, sending explicit unsolicited material to someone via email or messaging apps can attract Section 67.',
                'First conviction: Imprisonment up to 3 years, fine up to ₹5 Lakhs. Subsequent conviction: Imprisonment up to 5 years, fine up to ₹10 Lakhs.',
                'Content Regulation'
            ),
            (
                'section-67a',
                'Publishing Sexually Explicit Content',
                'Section 67A',
                'Section 67A is a stronger provision than Section 67, specifically targeting sexually explicit acts and conduct (not just obscene content). It covers publishing, transmitting, or causing to be published or transmitted material which contains sexually explicit acts. This section carries heavier punishment reflecting the serious nature of such content.',
                'Someone records a sexual act and uploads it to a pornographic website for public viewing, or shares explicit video clips of real people via WhatsApp groups. Such acts of publishing or distributing sexually explicit content are covered under Section 67A.',
                'First conviction: Imprisonment up to 5 years, fine up to ₹10 Lakhs. Subsequent conviction: Imprisonment up to 7 years, fine up to ₹10 Lakhs.',
                'Content Regulation'
            ),
            (
                'section-67b',
                'Child Pornography (CSAM)',
                'Section 67B',
                'Section 67B is India\'s strongest provision against child sexual abuse material (CSAM) online. It makes it illegal to publish, transmit, browse, download, or create material depicting children in sexually explicit situations. It also covers online grooming of children for sexual purposes. This section has zero tolerance and the harshest punishments.',
                'Anyone who downloads, shares, or even browses websites containing sexual content involving minors commits an offense under Section 67B. An adult who uses online chat platforms to lure minors into sharing intimate content is also liable under this section for grooming.',
                'First conviction: Imprisonment up to 5 years, fine up to ₹10 Lakhs. Subsequent conviction: Imprisonment up to 7 years, fine up to ₹10 Lakhs. Under POCSO Act, punishment can be more severe.',
                'Child Safety'
            ),
            (
                'section-72',
                'Breach of Confidentiality and Privacy',
                'Section 72',
                'Section 72 applies to persons who have been granted access to electronic records, books, registers, correspondence, information, documents, or other material under the powers conferred by the IT Act. It makes it illegal for such authorized persons to disclose that information to others without the consent of the person concerned. This is essentially a breach of trust provision for officials and certifying authorities.',
                'An employee of a Certifying Authority (like a digital certificate provider) who has access to clients\' private keys and sensitive information shares that data with a competitor for money. A government official who accesses citizens\' Aadhaar data for legitimate purposes but then leaks it is liable under Section 72.',
                'Imprisonment up to 2 years, or fine up to ₹1 Lakh, or both.',
                'Confidentiality'
            ),
        ]
        
        db.executemany('''
            INSERT INTO laws (slug, title, section, description, example, punishment, category)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', laws_data)
        db.commit()
    
    db.close()

# ─── Translation Data ──────────────────────────────────────────────────────────

# Simple translation dictionary for UI elements
TRANSLATIONS = {
    'en': {
        'home': 'Home',
        'laws': 'Laws',
        
        'feedback': 'Feedback',
        'search_placeholder': 'Search laws by name or section...',
        'listen': 'Listen',
        'section': 'Section',
        'punishment': 'Punishment & Penalty',
        'example': 'Real-life Example',
        'explanation': 'Explanation',
        'back_to_laws': 'Back to All Laws',
        
        'submit': 'Submit',
        'your_name': 'Your Name',
        'your_message': 'Your Message',
    },
    'hi': {
        'home': 'होम',
        'laws': 'कानून',
        
        'feedback': 'प्रतिक्रिया',
        'search_placeholder': 'नाम या अनुभाग द्वारा कानून खोजें...',
        'listen': 'सुनें',
        'section': 'अनुभाग',
        'punishment': 'सजा और जुर्माना',
        'example': 'वास्तविक जीवन का उदाहरण',
        'explanation': 'व्याख्या',
        'back_to_laws': 'सभी कानूनों पर वापस जाएं',
        
        'submit': 'जमा करें',
        'your_name': 'आपका नाम',
        'your_message': 'आपका संदेश',
    },
    'mr': {
        'home': 'मुखपृष्ठ',
        'laws': 'कायदे',
        
        'feedback': 'अभिप्राय',
        'search_placeholder': 'नाव किंवा विभागाने कायदे शोधा...',
        'listen': 'ऐका',
        'section': 'विभाग',
        'punishment': 'शिक्षा आणि दंड',
        'example': 'वास्तविक जीवनाचे उदाहरण',
        'explanation': 'स्पष्टीकरण',
        'back_to_laws': 'सर्व कायद्यांवर परत जा',
       
        'submit': 'सादर करा',
        'your_name': 'तुमचे नाव',
        'your_message': 'तुमचा संदेश',
    }
}



# ─── Routes ───────────────────────────────────────────────────────────────────

@app.route('/')
def index():
    """Homepage route."""
    db = get_db()
    # Get a few featured laws for homepage
    featured_laws = db.execute('SELECT * FROM laws LIMIT 6').fetchall()
    db.close()
    return render_template('index.html', featured_laws=featured_laws)

@app.route('/laws')
def laws():
    """Laws listing page."""
    db = get_db()
    all_laws = db.execute('SELECT * FROM laws ORDER BY id').fetchall()
    db.close()
    return render_template('laws.html', laws=all_laws)

@app.route('/law/<slug>')
def law_detail(slug):
    """Individual law detail page."""
    db = get_db()
    law = db.execute('SELECT * FROM laws WHERE slug = ?', (slug,)).fetchone()
    db.close()
    if not law:
        return "Law not found", 404
    return render_template('laws_detail.html', law=law)



@app.route('/feedback', methods=['GET', 'POST'])
def feedback():
    """Feedback form page."""
    if request.method == 'POST':
        data = request.get_json()
        name = data.get('name', '').strip()
        message = data.get('message', '').strip()
        
        if not name or not message:
            return jsonify({'success': False, 'error': 'Name and message are required.'})
        
        db = get_db()
        db.execute('INSERT INTO feedback (name, message) VALUES (?, ?)', (name, message))
        db.commit()
        db.close()
        return jsonify({'success': True, 'message': 'Thank you for your feedback!'})
    
    return render_template('feedback.html')

@app.route('/api/search')
def search():
    """Search laws by title or section."""
    query = request.args.get('q', '').strip()
    if not query:
        return jsonify([])
    
    db = get_db()
    results = db.execute(
        "SELECT slug, title, section, category FROM laws WHERE title LIKE ? OR section LIKE ? OR description LIKE ?",
        (f'%{query}%', f'%{query}%', f'%{query}%')
    ).fetchall()
    db.close()
    
    return jsonify([dict(r) for r in results])

@app.route('/api/translate', methods=['POST'])
def translate():
    """Translate law content using Google Cloud Translation API."""
    data = request.get_json()
    text = data.get('text', '')
    target_lang = data.get('lang', 'en')
    
    if target_lang == 'en' or not text:
        return jsonify({'translated': text, 'lang': 'en'})
    
    api_key = os.environ.get('VITE_GOOGLE_API_KEY')
    if not api_key:
        return jsonify({'translated': text, 'lang': 'en', 'note': 'Google API Key not found in .env'})

    try:
        url = f"https://translation.googleapis.com/language/translate/v2?key={api_key}"
        payload = {
            'q': text,
            'target': target_lang,
            'format': 'text'
        }
        res = requests.post(url, data=payload)
        res_data = res.json()
        
        if 'error' in res_data:
            return jsonify({'translated': text, 'lang': 'en', 'note': f"API Error: {res_data['error'].get('message', 'Unknown error')}"})

        translated_text = res_data['data']['translations'][0]['translatedText']
        return jsonify({'translated': translated_text, 'lang': target_lang})
    except Exception as e:
        return jsonify({'translated': text, 'lang': 'en', 'note': f'Translation service unavailable: {str(e)}'})

@app.route('/api/audio/<slug>')
def audio(slug):
    """Generate text-to-speech audio using Google Cloud TTS API."""
    db = get_db()
    law = db.execute('SELECT * FROM laws WHERE slug = ?', (slug,)).fetchone()
    db.close()
    
    if not law:
        return "Law not found", 404
        
    lang = request.args.get('lang', 'en')
    api_key = os.environ.get('VITE_GOOGLE_API_KEY')
    
    if not api_key:
        return jsonify({'error': 'Google API Key not found in .env'}), 500

    # Map language codes for Google TTS
    locale_map = {'en': 'en-IN', 'hi': 'hi-IN', 'mr': 'mr-IN'}
    tts_lang = locale_map.get(lang, 'en-US')
    
    text = f"{law['title']}. {law['section']}. {law['description']}"

    try:
        url = f"https://texttospeech.googleapis.com/v1/text:synthesize?key={api_key}"
        payload = {
            "input": {"text": text},
            "voice": {"languageCode": tts_lang},
            "audioConfig": {"audioEncoding": "MP3"}
        }
        
        res = requests.post(url, json=payload)
        data = res.json()
        
        if 'error' in data:
            return jsonify({'error': f"TTS API Error: {data['error'].get('message', 'Unknown error')}"}), 500
            
        if 'audioContent' in data:
            import base64
            audio_content = base64.b64decode(data['audioContent'])
            audio_fp = io.BytesIO(audio_content)
            audio_fp.seek(0)
            return send_file(audio_fp, mimetype='audio/mpeg', as_attachment=False)
        else:
            return jsonify({'error': 'Failed to generate audio content'}), 500
            
    except Exception as e:
        return jsonify({'error': f'TTS request failed: {str(e)}'}), 500

@app.route('/api/translations/<lang>')
def get_translations(lang):
    """Get UI translations for a language."""
    translations = TRANSLATIONS.get(lang, TRANSLATIONS['en'])
    return jsonify(translations)



# ─── Main ─────────────────────────────────────────────────────────────────────

if __name__ == '__main__':
    init_db()
    app.run(debug=True, port=5000)