import re
from .RAG_engine import RAGEngine


# ─────────────────────────────────────────────
#  TOLL-FREE NUMBERS (per card type)
# ─────────────────────────────────────────────
HELPLINES = {
    "abha": {
        "name"   : "ABHA / ABDM Helpline",
        "number" : "1800-11-4477",
        "website": "abdm.gov.in",
        "hours"  : "Mon-Sat, 8 AM to 8 PM",
        "email"  : "abdm@nha.gov.in"
    },
    "ayushman": {
        "name"   : "Ayushman Bharat PM-JAY",
        "number" : "14555",
        "website": "pmjay.gov.in",
        "hours"  : "24 x 7, All Days",
        "email"  : "pmjay@nha.gov.in"
    },
    "covid": {
        "name"   : "CoWIN COVID Helpline",
        "number" : "1075",
        "website": "www.cowin.gov.in",
        "hours"  : "24 x 7, All Days",
        "email"  : "support@cowin.gov.in"
    },
    "aarogyaone": {
        "name"   : "AarogyaOne App Support",
        "number" : "1800-XXX-XXXX",
        "website": "aarogyaone on Play Store",
        "hours"  : "Mon-Fri, 9 AM to 6 PM",
        "email"  : "support@jdeanzhealthtech.com"
    }
}

APP_LINK = "https://play.google.com/store/apps/details?id=com.jdeanzhealthtech.aarogyaone"
DIV      = ""  # Removed lines for professional structure

INITIAL_GREETING = (
    f"\n**Namaste! Welcome to AarogyaOne PHR Support.**\n\n"
    f"I am your AI assistant here to help you with your digital health needs. "
    f"Please select your preferred language for conversation:\n\n"
    f"1. **English** (या \"English\" टाइप करें)\n"
    f"2. **Hindi (हिंदी)** (या \"Hindi\" टाइप करें)\n"
    f"3. **Gujarati (ગુજરાતી)** (या \"Gujarati\" તાઈપ કરો)\n\n"
    f"Type **1**, **2**, or **3** OR type the language name to continue.\n"
    f"\n---\n"
    f"You can ask me about:\n"
    f"📋 **ABHA Card**: How to create or download your 14-digit Health ID.\n"
    f"🥇 **Ayushman Bharat**: Pm-JAY claim history.\n"
    f"💉 **COVID Certificate**: Fast steps to download your vaccination proof.\n"
    f"📱 **AarogyaOne App**: Help with medical record uploads and doctor appointments.\n"
    f"📞 **Helplines**: Instant access to emergency and medical support numbers.\n"
)

# Translations for UI and Templates
LANG_DATA = {
    "en": {
        "info": "Information", "steps": "Steps", "note": "Note", "link": "Link", "helpline": "HELPLINE",
        "toll_free": "Toll-Free", "website": "Website", "hours": "Hours", "email": "Email",
        "greet": "Namaste! Welcome to AarogyaOne", "help_list": "I can help you with:",
        "ask_assist": "How can I assist you today?", "goodbye": "Thank You! Stay Healthy!",
        "stay_touch": "See you again. Take care!", "welcome": "You Are Welcome!",
        "anything_else": "Anything else I can help you with?", "emergency": "EMERGENCY — CALL IMMEDIATELY!",
        "emergency_warn": "Do NOT use chatbot in emergencies!", "emergency_call": "Call 108 RIGHT NOW!",
        "fix_steps": "Quick Fix Steps:", "still_not_working": "Still not working? Call App Support:",
        "abha_name": "ABHA Card", "ayushman_name": "Ayushman Card", "covid_name": "COVID Certificate",
        "app_name": "AarogyaOne App", "medical_name": "Medical Queries",
        "satisfaction": "Do you have any other questions? (Yes / No)",
        "otp_issue": "AADHAAR OTP Issue", "lab_report": "Lab Reports & Records",
    },
    "hi": {
        "info": "जानकारी", "steps": "कदम", "note": "नोट", "link": "लिंक", "helpline": "हेल्पलाइन",
        "toll_free": "टोल-फ्री", "website": "वेबसाइट", "hours": "समय", "email": "ईमेल",
        "greet": "नमस्ते! AarogyaOne में आपका स्वागत है", "help_list": "मैं इन विषयों में मदद कर सकता हूँ:",
        "ask_assist": "आज मैं आपकी कैसे मदद कर सकता हूँ?", "goodbye": "धन्यवाद! स्वस्थ रहें!",
        "stay_touch": "फिर मिलेंगे। अपना ख्याल रखें!", "welcome": "आपका स्वागत है!",
        "anything_else": "क्या मैं किसी और चीज में मदद कर सकता हूँ?", "emergency": "आपातकाल — तुरंत कॉल करें!",
        "emergency_warn": "आपातकाल में चैटबॉट का उपयोग न करें!", "emergency_call": "अभी 108 पर कॉल करें!",
        "fix_steps": "त्वरित समाधान कदम:", "still_not_working": "अभी भी काम नहीं कर रहा है? सहायता को कॉल करें:",
        "abha_name": "ABHA कार्ड", "ayushman_name": "आयुष्मान कार्ड", "covid_name": "COVID प्रमाणपत्र",
        "app_name": "AarogyaOne ऐप", "medical_name": "चिकित्सा प्रश्न",
        "satisfaction": "क्या आपका कोई और सवाल है? (Yes / No)",
        "otp_issue": "आधार OTP समस्या", "lab_report": "लैब रिपोर्ट और रिकॉर्ड",
    },
    "gu": {
        "info": "માહિતી", "steps": "પગલાં", "note": "નોટ", "link": "લિંક", "helpline": "હેલ્પલાઈન",
        "toll_free": "ટોલ-ફ્રી", "website": "વેબસાઇટ", "hours": "સમય", "email": "ઇમેઇલ",
        "greet": "નમસ્તે! AarogyaOne માં તમારું સ્વાગત છે", "help_list": "હું આ વિષયોમાં મદદ કરી શકું છું:",
        "ask_assist": "આજે હું તમને કેવી રીતે મદદ કરી શકું?", "goodbye": "આભાર! સ્વસ્થ રહો!",
        "stay_touch": "આવજો. તમારું ધ્યાન રાખજો!", "welcome": "તમારું સ્વાગત છે!",
        "anything_else": "બીજું કોઈ મદદ જોઈએ છે?", "emergency": "આપતકાલ — તુરંત કૉલ કરો!",
        "emergency_warn": "આપતકાલમાં ચેટબોટનો ઉપયોગ ન કરો!", "emergency_call": "હજી 108 ને કૉલ કરો!",
        "fix_steps": "ઝડપી ઠીક માટે પગલાં:", "still_not_working": "હજી કામ નથી કરતું? આધાર લાઇનને કૉલ કરો:",
        "abha_name": "ABHA કાર્ડ", "ayushman_name": "આયુષ્માન કાર્ડ", "covid_name": "COVID પ્રમાણપત્ર",
        "app_name": "AarogyaOne એપ્લિકેશન", "medical_name": "તબીબી પ્રશ્નો",
        "satisfaction": "શું તમારો કોઈ અન્ય પ્રશ્ન છે? (Yes / No)",
        "otp_issue": "આધાર OTP સમસ્યા", "lab_report": "લેબ રિપોર્ટ્સ અને રેકોર્ડ્સ",
    },
    "pa": {
        "info": "Jaankari", "steps": "Steps", "note": "Note", "link": "Link", "helpline": "HELPLINE",
        "toll_free": "Toll-Free", "website": "Website", "hours": "Samay", "email": "Email",
        "greet": "Satsriakal! AarogyaOne vich tuhada swagat hai", "help_list": "Main ena kamma vich madad kar sakda han:",
        "ask_assist": "Main tuhadi kiven madad kar sakda han?", "goodbye": "Dhanwad! Swasth raho!",
        "stay_touch": "Phir milange. Apna khayal rakho!", "welcome": "Tuhada swagat hai!",
        "anything_else": "Hor koi madad chahidi hai?", "emergency": "EMERGENCY — TURANT CALL KARO!",
        "emergency_warn": "Emergency vich chatbot di varton na karo!", "emergency_call": "Hune 108 te call karo!",
        "fix_steps": "Quick Fix Steps:", "still_not_working": "Haje vi kamm nahi kar reha? Support nu call karo:",
        "abha_name": "ABHA Card", "ayushman_name": "Ayushman Card", "covid_name": "COVID Certificate",
        "app_name": "AarogyaOne App",
    }
}


def helpline_box(card_type, lang="en"):
    """Return a single line helpline info"""
    h = HELPLINES.get(card_type, HELPLINES["abha"])
    ld = LANG_DATA.get(lang, LANG_DATA["en"])
    return (
        f"\n📞 **{ld['helpline']}**: {h['name']} | ☎ {h['number']} | 🌐 {h['website']}\n"
    )


def S(title, icon, rows=None, note=None, links=None, card_helpline=None, warn=None, lang="en"):
    """
    Build a consistent structured response with bold headings.
    """
    ld = LANG_DATA.get(lang, LANG_DATA["en"])
    out = [f"\n{icon} **{title}**\n"]
    if warn:
        out.append(f"⚠️ **{warn}**")
    if rows:
        out.append(f"\n**{ld['steps']}:**" if "Download" in title or "Create" in title else f"\n**{ld['info']}:**")
        for i, r in enumerate(rows, 1):
            out.append(f"  {i}. {r}")
    if links:
        out.append(f"\n**{ld['link']}:**")
        for label, url in links:
            out.append(f"  🔗 {label}: {url}")
    if note:
        out.append(f"\n💡 **{ld['note']}**: {note}")
    if card_helpline:
        out.append(helpline_box(card_helpline, lang))
    
    # Add satisfaction message at the end
    out.append(f"\n{ld['satisfaction']}")
    return "\n".join(out)


def out_of_scope(user_input, lang="en"):
    """Response for questions we cannot answer"""
    ld = LANG_DATA.get(lang, LANG_DATA["en"])
    q = user_input[:70] + ("..." if len(user_input) > 70 else "")
    
    # Proper translations for out of scope based on language
    if lang == "gu":
        title = "આભાર!"
        msg = "તમારો પ્રશ્ન અમાર સહાય ટીમને મળી છે. તેઓ તમારા સાથે જલ્દીથી સંપર્ક કરશે."
        direct = "તાત્કાલિક મદદ માટે તમને સીધું કૉલ કરો:"
        topics = "હું આ વિષયો પર મદદ કરી શકું છું:"
    elif lang == "hi":
        title = "धन्यवाद!"
        msg = "आपका सवाल हमारी सहायता टीम तक पहुंच गया है। वह जल्द ही आपसे संपर्क करेंगे।"
        direct = "तुरंत मदद के लिए सीधे कॉल करें:"
        topics = "मैं इन विषयों पर मदद कर सकता हूँ:"
    else:
        title = "Thank You!"
        msg = "Your query has been logged with our support team. They will connect with you shortly."
        direct = "For urgent help, contact us directly:"
        topics = "Topics I can answer right now:"

    return (
        f"\n{DIV}\n"
        f"  🙏  {title}\n"
        f"{DIV}\n"
        f"\n  ✅  {msg}\n"
        f"  ❝ {q} ❞\n"
        f"\n  {direct}\n"
        f"  ☎   Helpline  :  1800-11-4477\n"
        f"  📧  Email     :  support@aarogyaone.in\n"
        f"\n  {topics}\n"
        f"  📋  ABHA Card      🥇  Ayushman Card\n"
        f"  💉  COVID Cert     📱  AarogyaOne App\n"
        f"{DIV}\n"
    )


class AarogyaChatbot:
    def __init__(self):
        # Load knowledge base from multiple JSON files (*_base.json)
        self.rag = RAGEngine(knowledge_base_path="../data", use_multiple_files=True)
        self.conversation_history = []
        self.selected_lang = None  # Persistent language choice
        self.pending_category = None  # Track if user selected a general category
        self.pending_questions = {}  # Map A, B, C to doc IDs
        
        # Main category display names
        self.category_names = {
            "abha": "ABHA Card",
            "ayushman": "Ayushman Bharat",
            "covid": "COVID Certificate",
            "aarogyaone": "AarogyaOne App"
        }
        
        # Sub-categories for each main category (Keyword-based)
        self.category_subcategories = {
            "abha": {
                "create": {"keywords": r"\b(creat|bana|register|make|new|naya)\b", "en": "How to create ABHA Card"},
                "download": {"keywords": r"\b(download|get|le|dikhao)\b", "en": "How to download ABHA Card"},
                "otp_issue": {"keywords": r"\b(otp|adhar|aadhar|aadhaar|verify)\b", "en": "AADHAAR OTP Issue"}
            },
            "ayushman": {
                "get": {"keywords": r"\b(get|apply|milna|registration)\b", "en": "How to get Ayushman Card"},
                "download": {"keywords": r"\b(download|golden|le|nikale)\b", "en": "How to download Ayushman Card"},
                "coverage": {"keywords": r"\b(coverage|cover|lakh|benefit|fayde)\b", "en": "Ayushman Card Benefits"}
            },
            "covid": {
                "download": {"keywords": r"\b(download|cert|vaccine|le)\b", "en": "How to download COVID Certificate"}
            },
            "aarogyaone": {
                "download": {"keywords": r"\b(download|install|get|app)\b", "en": "How to download AarogyaOne App"},
                "upload": {"keywords": r"\b(upload|add|document|report)\b", "en": "How to upload documents"},
                "appointment": {"keywords": r"\b(appointment|book|doctor|consult)\b", "en": "How to book appointment"}
            }
        }
        
        self.intents = {
            "greet":             r"\b(hi+|hello|hey|namaste|namaskar|kem cho|satsriakal)\b",
            "goodbye":           r"\b(bye|goodbye|exit|quit|see you|alvida|tata)\b",
            "app_not_working":   r"(app.*(not work|crash|error|open|load|issue|problem|start|nahi chal raha))\b",
            "abha_download":     r"(d[ow]{1,2}nl[oa]{1,2}d.*abha|abha.*d[ow]{1,2}nl[oa]{1,2}d)",
            "abha_create":       r"(abha.*(creat[e]?|register|make|apply|new|bana))",
            "abha_otp_issue":    r"((otp|adhar otp|aadhar otp).*issue|otp.*nahi.*aa.*raha)",
            "ayushman_get":      r"(ayushman.*(kaise.*(mile|banaye)|apply|eligib|prapt))",
            "ayushman_download": r"(ayushman.*d[ow]{1,2}nl[oa]{1,2}d|golden.*card)",
            "ayushman_coverage": r"(benefi|coverag|fayda|fayde|faida|labh|lakh.*cover)",
            "covid_download":    r"(covid.*(certificate|cert|certi|d[ow]{1,2}nl[oa]{1,2}d|vaccination|le))",
            "app_download":      r"(d[ow]{1,2}nl[oa]{1,2}d.*app|app.*d[ow]{1,2}nl[oa]{1,2}d|install.*aarogya)",
            "app_upload":        r"(upload|add.*document|prescription.*upload|report.*upload)",
            "app_appointment":   r"(appointment|book|doctor.*milna|doctor.*dikhao)",
            "app_link_abha":     r"(link.*abha|abha.*connect|abha.*kaise.*jodein)",
            "emergency":         r"\b(emergency|urgent|serious|critical|chest pain|blood|heart attack)\b",
            "helpline":          r"\b(helpline|toll free|contact|phone|call|number)\b",
            "thanks":            r"\b(thank|thanks|shukriya|dhanyawad|thnx|thx)\b",
        }

    def detect_language(self, text):
        t = text.lower()
        scores = {"gu": 0, "hi": 0, "pa": 0, "en": 0}
        if re.search(r"\b(che|shu|kem|joiye|nathi|karvu|karo|ne)\b", t): scores["gu"] += 5
        if re.search(r"\b(hai|kya|kaise|karna|chaiye|hoga|kariye)\b", t): scores["hi"] += 3
        if re.search(r"\b(ki|kiven|kithe|duso|chahida|si|han)\b", t): scores["pa"] += 5
        if re.search(r"\b(how|what|download|app|cert|get)\b", t): scores["en"] += 2
        best_lang = max(scores, key=scores.get)
        return best_lang if scores[best_lang] > 0 else "en"

    def format_answer_with_steps(self, content):
        """Automatically number instructions in the content as Step 1, Step 2, etc."""
        sentences = re.split(r'\.\s+', content.strip())
        formatted_sentences = []
        step_count = 1
        step_keywords = r"\b(visit|go to|open|click|enter|type|submit|download|select|choose|verify|login|register|fill|check|use)\b"
        
        for sentence in sentences:
            if not sentence: continue
            if re.search(step_keywords, sentence, re.IGNORECASE):
                formatted_sentences.append(f"Step {step_count}: {sentence.strip()}")
                step_count += 1
            else:
                formatted_sentences.append(sentence.strip())
        
        # Rejoin with newlines for better readability
        result = "\n".join(formatted_sentences)
        return result

    def ask_topic_questions(self, category, lang="en"):
        """Show all questions for a category with A, B, C, D labels"""
        docs = self.rag.get_all_documents_by_category(category)
        if not docs: return None
        
        self.pending_category = category
        self.pending_questions = {}
        
        title = self.category_names.get(category, category.upper())
        response = f"\n{DIV}\n  ❓  **{title} - Select a question:**\n{DIV}\n\n"
        
        for i, doc in enumerate(docs):
            label = chr(65 + i)  # A, B, C...
            self.pending_questions[label] = doc["id"]
            response += f"  **{label}**. {doc['title']}\n"
        
        response += f"\n{DIV}\n  Type the letter (**A, B, C...**) to see the answer.\n"
        return response

    def detect_intent(self, text):
        t = text.lower().strip()
        found = []
        for intent, pattern in self.intents.items():
            if re.search(pattern, t, re.IGNORECASE):
                found.append(intent)
        return found if found else ["unknown"]

    def get_main_category(self, intents):
        for intent in intents:
            if intent.startswith("abha"): return "abha"
            elif intent.startswith("ayushman"): return "ayushman"
            elif intent.startswith("covid"): return "covid"
            elif intent.startswith("app"): return "aarogyaone"
        return None

    def ask_subcategory(self, category, lang="en"):
        # Legacy sub-category logic (used as fallback or for small queries)
        subcats = self.category_subcategories.get(category, {})
        msg = f"What would you like to know about {self.category_names.get(category, category)}?"
        response = f"\n{DIV}\n  ❓  {msg}\n{DIV}\n\n"
        for sub_key, sub_data in subcats.items():
            sub_label = sub_data.get(lang, sub_data.get("en", sub_key))
            response += f"  - {sub_label}\n"
        self.pending_category = category
        return response

    def match_subcategory(self, user_input, category, lang="en"):
        t = user_input.lower().strip()
        subcats = self.category_subcategories.get(category, {})
        for sub_key, sub_data in subcats.items():
            keywords = sub_data.get("keywords", "").lower()
            if any(k.strip() in t for k in keywords.replace(r'\b(', '').replace(r')\b', '').split('|') if k.strip()):
                return sub_key, sub_data.get(lang, sub_data.get("en"))
        return None, None

    def get_rag_response(self, query, min_score=0.15, lang="en"):
        best, answers = self.rag.get_answer(query, top_k=2)
        if not answers or answers[0]["score"] < min_score: return None
        lines = [l.strip() for l in best.strip().split(". ") if l.strip()]
        ld = LANG_DATA.get(lang, LANG_DATA["en"])
        question = ld.get("satisfaction", "Do you have any other questions? (Yes / No)")
        return f"\n{DIV}\n  ℹ️   Information\n{DIV}\n\n" + "\n".join(f"  {l}" for l in lines) + f"\n{DIV}\n\n  ❓  {question}\n"

    def build_response(self, intents, user_input, lang="en"):
        responses = []
        ld = LANG_DATA.get(lang, LANG_DATA["en"])
        
        if "greet" in intents:
            if self.selected_lang:
                responses.append(
                    f"\n{DIV}\n  👋  {ld['greet']}\n{DIV}\n"
                    f"\n  {ld['ask_assist']}\n  {ld['help_list']}\n"
                    f"  1. **ABHA Card**\n  2. **Ayushman Bharat**\n"
                    f"  3. **COVID Certificate**\n  4. **AarogyaOne App**\n"
                    f"\n  Type **1, 2, 3, or 4** to see all details.\n{DIV}\n"
                )
            else: responses.append(INITIAL_GREETING)
        
        if "emergency" in intents:
            return (f"\n{'═' * 52}\n  🚨  {ld['emergency']}\n{'═' * 52}\n"
                    f"\n  🚑  Ambulance: 108 | 🏥  Health Helpline: 104\n"
                    f"\n  ⚠️   {ld['emergency_warn']}\n  ⚠️   {ld['emergency_call']}\n{'═' * 52}\n")

        for intent in intents:
            if intent in ["greet", "emergency", "unknown"]: continue
            if intent == "goodbye":
                responses.append(f"\n{DIV}\n  👋  {ld['goodbye']}\n{DIV}\n\n  📱  Download App: {APP_LINK}\n  💚  {ld['stay_touch']}\n{DIV}\n")
            elif intent == "thanks":
                responses.append(f"\n{DIV}\n  😊  {ld['welcome']}\n{DIV}\n\n  {ld['anything_else']}\n  📱  {APP_LINK}\n{DIV}\n")
            elif intent == "abha_info":
                responses.append(S(f"{ld['abha_name']} Summary", "🏥", rows=["ABHA is a 14-digit unique health ID", "Store medical records digitally", "To Create: Type 1 -> A", "To Download: Type 1 -> B"], lang=lang, card_helpline="abha"))
            elif intent == "ayushman_info":
                responses.append(S(f"{ld['ayushman_name']} Summary", "🥇", rows=["Free health cover up to Rs 5 Lakh", "Valid at gov & private hospitals", "To Get: Type 2 -> A"], lang=lang, card_helpline="ayushman"))
            elif intent == "covid_info": return self.ask_topic_questions("covid", lang)
            elif intent == "app_info":
                responses.append(S(f"Summary: {ld['app_name']}", "📱", rows=["Manage health records", "Book doctor appointments", "Link ABHA"], lang=lang, card_helpline="aarogyaone"))
            elif intent == "app_appointment":
                rows = ["Open AarogyaOne app", "Go to Doctor section", "Search and select doctor", "Choose slot and book"]
                responses.append(S(f"{ld['app_name']} Appointment", "📅", rows=rows, lang=lang, card_helpline="aarogyaone"))
            elif intent == "app_link_abha":
                rows = ["Login to AarogyaOne", "Go to Profile/ABHA section", "Enter ABHA or Aadhaar", "Verify with OTP"]
                responses.append(S(f"Link ABHA with {ld['app_name']}", "🔗", rows=rows, lang=lang, card_helpline="aarogyaone"))
            elif intent == "abha_download":
                rows = ["Visit abdm.gov.in", "Enter mobile/ABHA", "Verify OTP", "Download PDF"]
                responses.append(S(f"{ld['abha_name']} Download", "📥", rows=rows, lang=lang, card_helpline="abha"))
            elif intent == "abha_create":
                rows = ["Visit abdm.gov.in", "Enter Aadhaar Number", "Verify OTP", "Fill details and download"]
                responses.append(S(f"{ld['abha_name']} Create", "📝", rows=rows, lang=lang, card_helpline="abha"))
            elif intent == "app_not_working":
                responses.append(f"\n⚠️ **{ld['app_name']} Issue?**\n\n**{ld['fix_steps']}**\n  1. Reopen app | 2. Check Net | 3. Update App\n\n**{ld['still_not_working']}**{helpline_box('aarogyaone', lang)}")
            elif intent == "helpline":
                responses.append(f"\n📞 **Helplines**: Amb: 108 | ABHA: 1800-11-4477 | Ayushman: 14555 | CoWIN: 1075\n")

        if not responses:
            rag = self.get_rag_response(user_input, lang=lang)
            return rag if rag else out_of_scope(user_input, lang)
        return "\n".join(responses)

    def handle_feedback(self, text, lang="en"):
        t = text.lower().strip()
        if self.detect_intent(text) != ["unknown"]: return None
        if re.search(r"^(yes|yep|yeah|sure|ha|haan|jee|ji)\b", t):
            ld = LANG_DATA.get(lang, LANG_DATA["en"])
            return f"\n{DIV}\n  👋  {ld['greet']}\n{DIV}\n\n  {ld['ask_assist']}\n  1. ABHA | 2. Ayushman | 3. COVID | 4. App\n"
        if re.search(r"^(no|nope|na|nahi|nathi)\b", t):
            ld = LANG_DATA.get(lang, LANG_DATA["en"])
            return f"\n{DIV}\n  👋  {ld['goodbye']}\n{DIV}\n\n  📱  Download App: {APP_LINK}\n"
        return None
    
    def chat(self, user_input):
        user_input = user_input.strip()
        if not user_input: return "🤔 Type a message."

        # 1. Handle selection by number
        if user_input in ["1", "2", "3", "4"]:
            if not self.selected_lang:
                if user_input == "4": return "🤔 Please select 1, 2, or 3 for language."
                lang_map = {"1": "en", "2": "hi", "3": "gu"}
                self.selected_lang = lang_map[user_input]
                ld = LANG_DATA.get(self.selected_lang, LANG_DATA["en"])
                return f"\n✅ **Language set!**\n\n  {ld['help_list']}\n  1. ABHA Card | 2. Ayushman | 3. COVID | 4. App"
            else:
                category_map = {"1": "abha", "2": "ayushman", "3": "covid", "4": "aarogyaone"}
                return self.ask_topic_questions(category_map[user_input], self.selected_lang)

        # 2. Handle selection by letter (A, B, C...)
        user_choice = user_input.upper().strip()
        if self.pending_questions and user_choice in self.pending_questions:
            doc_id = self.pending_questions[user_choice]
            doc = next((d for d in self.rag.documents if d.get("id") == doc_id), None)
            if doc:
                formatted_ans = self.format_answer_with_steps(doc["content"])
                ld = LANG_DATA.get(self.selected_lang or "en", LANG_DATA["en"])
                self.pending_category = None; self.pending_questions = {}
                return f"\n{DIV}\n  **{doc['title']}**\n{DIV}\n\n{formatted_ans}\n\n{ld['satisfaction']}"

        # 3. Handle persistent language
        lang = self.selected_lang if self.selected_lang else self.detect_language(user_input)
        
        # 4. Feedback
        feedback = self.handle_feedback(user_input, lang)
        if feedback: return feedback

        # 5. Intent detection
        intents = self.detect_intent(user_input)
        main_category = self.get_main_category(intents)
        
        # 6. Topic menu trigger
        if main_category and len(user_input.split()) <= 2:
            return self.ask_topic_questions(main_category, lang)
            
        return self.build_response(intents, user_input, lang)


if __name__ == "__main__":
    bot = AarogyaChatbot()
    print("      🏥  AarogyaOne Medical AI Chatbot")
    print(bot.chat("hello"))
    while True:
        try:
            msg = input("\nYou: ").strip()
            if msg.lower() in ["exit", "bye"]: break
            print(bot.chat(msg))
        except EOFError: break
