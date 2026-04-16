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
    f"3. **Gujarati (ગુજરાતી)** (या \"Gujarati\" टाइप करें)\n\n"
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
        "anything_else": "બીજું કોઈ મદદ જોઈએ છે?", "emergency": "આપતકાલ — તુરંત કॉલ કરો!",
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
        f"  •  ABHA Card      •  Ayushman Card\n"
        f"  •  COVID Cert     •  AarogyaOne App\n"
        f"{DIV}\n"
    )


class AarogyaChatbot:
    def __init__(self):
        # Load knowledge base from multiple JSON files (*_base.json)
        # Falls back to single file if folder not found
        self.rag = RAGEngine(knowledge_base_path="../data", use_multiple_files=True)
        self.conversation_history = []
        self.selected_lang = None  # Persistent language choice
        self.pending_category = None  # Track if user selected a general category
        
        # Sub-categories for each main category
        self.category_subcategories = {
            "abha": {
                "create": {
                    "keywords": r"\b(creat|bana|register|make|new|naya|nayo|nava|start|apply|signup|sign up)\b",
                    "en": "How to create ABHA Card",
                    "hi": "ABHA कार्ड कैसे बनाएं",
                    "gu": "ABHA કાર્ડ કેવી રીતે બનાવવું"
                },
                "download": {
                    "keywords": r"\b(download|d[ow]{1,2}nl|get|le|dikhao|show|dhao|prapt|praapti|download)\b",
                    "en": "How to download ABHA Card",
                    "hi": "ABHA कार्ड कैसे डाउनलोड करें",
                    "gu": "ABHA કાર્ડ કેવી રીતે ડાઉનલોડ કરવું"
                },
                "otp_issue": {
                    "keywords": r"\b(otp|adhar|aadhar|aadhaar|verification|verify|samasya|issue|problem|nahi aa|not coming|wrong)\b",
                    "en": "AADHAAR OTP Issue",
                    "hi": "AADHAAR OTP समस्या",
                    "gu": "AADHAAR OTP સમસ્યા"
                },
                "other": {
                    "keywords": r"\b(other|aur|kuch|and|anything|else|alag|alava|more|aetran)\b",
                    "en": "Other ABHA Issues",
                    "hi": "अन्य ABHA समस्याएं",
                    "gu": "અન્ય ABHA સમસ્યાઓ"
                }
            },
            "ayushman": {
                "get": {
                    "keywords": r"\b(get|get|ptrapt|register|apply|enrollment|milna|mil|apply|registration)\b",
                    "en": "How to get Ayushman Card",
                    "hi": "Ayushman कार्ड कैसे प्राप्त करें",
                    "gu": "Ayushman કાર્ડ કેવી રીતે મેળવવું"
                },
                "download": {
                    "keywords": r"\b(download|d[ow]{1,2}nl|get|le|dikhao|show)\b",
                    "en": "How to download Ayushman Card",
                    "hi": "Ayushman कार्ड कैसे डाउनलोड करें",
                    "gu": "Ayushman કાર્ડ કેવી રીતે ડાઉનલોડ કરવું"
                },
                "coverage": {
                    "keywords": r"\b(coverage|cover|lakh|treatment|cost|benefits|fayde|fayda|benifits|coverages|benefit|faida|faide|advantages|kya|kya milega)\b",
                    "en": "Ayushman Card Benefits & Coverage",
                    "hi": "Ayushman कार्ड लाभ और कवरेज",
                    "gu": "Ayushman કાર્ડ ફાયદા અને કવરેજ"
                },
                "other": {
                    "keywords": r"\b(other|aur|kuch|anything|else)\b",
                    "en": "Other Ayushman Issues",
                    "hi": "अन्य Ayushman समस्याएं",
                    "gu": "અન્ય Ayushman સમસ્યાઓ"
                }
            },
            "covid": {
                "download": {
                    "keywords": r"\b(download|d[ow]{1,2}nl|get|le|dikhao|show|certi|cert|certificate)\b",
                    "en": "How to download COVID Certificate",
                    "hi": "COVID प्रमाणपत्र कैसे डाउनलोड करें",
                    "gu": "COVID પ્રમાણપત્ર કેવી રીતે ડાઉનલોડ કરવું"
                },
                "lost_or_issue": {
                    "keywords": r"\b(lost|lose|issue|problem|nahi|not|received|missing|recover|retriev)\b",
                    "en": "COVID Certificate Lost or Not Received",
                    "hi": "COVID प्रमाणपत्र खो गया या प्राप्त नहीं हुआ",
                    "gu": "COVID પ્રમાણપત્ર ખોવાયું અથવા પ્રાપ્ત નથી"
                },
                "information": {
                    "keywords": r"\b(what|kya|information|details|about|baare|details|vistar)\b",
                    "en": "What is COVID Vaccination Certificate",
                    "hi": "COVID टीकाकरण प्रमाणपत्र क्या है",
                    "gu": "COVID કસોટી પ્રમાણપત્ર શું છે"
                },
                "other": {
                    "keywords": r"\b(other|aur|kuch|anything|else)\b",
                    "en": "Other COVID Issues",
                    "hi": "अन्य COVID समस्याएं",
                    "gu": "અન્ય COVID સમસ્યાઓ"
                }
            },
            "aarogyaone": {
                "download": {
                    "keywords": r"\b(download|d[ow]{1,2}nl|install|get|le|play store|app store)\b",
                    "en": "How to download AarogyaOne App",
                    "hi": "AarogyaOne ऐप कैसे डाउनलोड करें",
                    "gu": "AarogyaOne ઍપ કેવી રીતે ડાઉનલોડ કરવું"
                },
                "upload": {
                    "keywords": r"\b(upload|add|document|prescription|report|records|add|daal|save)\b",
                    "en": "How to upload documents in AarogyaOne",
                    "hi": "AarogyaOne में दस्तावेज़ कैसे अपलोड करें",
                    "gu": "AarogyaOne માં દસ્તાવેજો કેવી રીતે અપલોડ કરવા"
                },
                "appointment": {
                    "keywords": r"\b(appointment|book|doctor|meeting|schedule|consult|checkup|milna)\b",
                    "en": "How to book appointment in AarogyaOne",
                    "hi": "AarogyaOne में अपॉइंटमेंट कैसे बुक करें",
                    "gu": "AarogyaOne માં નિયુક્તિ કેવી રીતે બુક કરવી"
                },
                "link_abha": {
                    "keywords": r"\b(link|connect|join|jodein|sync|taal|connect|aarogyaone|app)\b",
                    "en": "How to link ABHA with AarogyaOne PHR app?",
                    "hi": "ABHA को AarogyaOne PHR ऐप के साथ कैसे लिंक करें?",
                    "gu": "ABHA ને AarogyaOne PHR એપ સાથે કેવી રીતે લિંક કરવું?"
                },
                "other": {
                    "keywords": r"\b(other|aur|kuch|anything|else)\b",
                    "en": "Other AarogyaOne Issues",
                    "hi": "अन्य AarogyaOne समस्याएं",
                    "gu": "અન્ય AarogyaOne સમસ્યાઓ"
                }
            }
        }
        
        self.intents = {
            "greet":             r"\b(hi+|hello|hey|namaste|namaskar|kem cho|satsriakal|adaab|helo|hey)\b",
            "goodbye":           r"\b(bye|goodbye|exit|quit|see you|alvida|tata|chalta hoon|avjo|rab rakha)\b",
            "app_not_working":   r"(app.*(not work|crash|error|open|load|issue|problem|start|nahi chal raha|kaam nahi kar|chalu nahi|nathi chaltu|nahi chalda))\b",
            "abha_download":     r"(d[ow]{1,2}nl[oa]{1,2}d.*abha|abha.*d[ow]{1,2}nl[oa]{1,2}d|abha.*kaise.*(le|nikale|d[ow]{1,2}nl[oa]{1,2}d)|abha.*kem.*d[ow]{1,2}nl[oa]{1,2}d|abha.*kiven.*d[ow]{1,2}nl[oa]{1,2}d)",
            "abha_create":       r"(abha.*(creat[e]?|crte|register|make|apply|new|bana)|creat[e,a]?.*abha|abha.*kaise.*bana|abha.*kem.*banavu|abha.*kiven.*banaye)",
            "abha_info":         r"\b(abha|health id|health account|14.digit|ye kya hai|shu che|ki hai|vistar)\b",
            "abha_otp_issue":    r"((otp|adhar otp|aadhar otp|aadhaar otp).*issue|otp.*nahi.*aa.*raha|otp.*problem|otp.*error)",
            "abha_other":        r"(other.*abha|abha.*other|aur.*abha|kuch.*aur.*abha|abha.*issue|abha.*problem)",
            "ayushman_get":      r"(ayushman.*(kaise.*(mile|milega|banaye|banvau|paye)|apply|eligib|prapt|banva|register)|how.*get.*ayushman|get.*ayushman.*card|ayushman.*card.*kaise|ayushman.*card.*kem)",
            "ayushman_download": r"(ayushman.*(d[ow]{1,2}nl[oa]{1,2}d|golden|le)|golden.*card|ayushman.*kaise.*(le|d[ow]{1,2}nl[oa]{1,2}d)|ayushman.*kem.*d[ow]{1,2}nl[oa]{1,2}d|ayushman.*kiven.*d[ow]{1,2}nl[oa]{1,2}d)",
            "ayushman_coverage": r"(benefi|coverag|fayda|fayde|faida|faide|labh|\blabh\b|lakh.*cover|cover.*lakh|kya.*milega|benifits|benifit|coverages)",
            "ayushman_info":     r"\b(ayushman|pmjay|jan arogya|5 lakh|health insurance|bima|scheme|yojana)\b",
            "covid_download":    r"(covid.*(certificate|cert|certi|d[ow]{1,2}nl[oa]{1,2}d|vaccination|le)|vaccine.*cert|covid.*kaise.*(le|d[ow]{1,2}nl[oa]{1,2}d)|covid.*kem.*d[ow]{1,2}nl[oa]{1,2}d|covid.*kiven.*d[ow]{1,2}nl[oa]{1,2}d)",
            "covid_info":        r"\b(covid|corona|vaccination|vaccine|covishield|covaxin|teeka|tika)\b",
            "app_download":      r"(d[ow]{1,2}nl[oa]{1,2}d.*app|app.*d[ow]{1,2}nl[oa]{1,2}d|install.*aarogya|play store|app.*kahan.*milega|app.*kem.*d[ow]{1,2}nl[oa]{1,2}d|app.*kiven.*d[ow]{1,2}nl[oa]{1,2}d)",
            "app_upload":        r"(upload|add.*document|prescription.*upload|report.*upload|file.*kaise.*daalein|kahan.*upload)",
            "app_appointment":   r"(appointment|book|doctor.*milna|doctor.*dikhao|checkup|meeting|schedule)",
            "app_link_abha":     r"(link.*abha|abha.*connect|abha.*kaise.*jodein|abha.*kem.*link|abha.*kiven.*link)",
            "app_share":         r"(share.*record|send.*record|doctor.*bhejo|whatsapp.*bhejo|file.*share)",
            "app_view":          r"(view.*record|see.*record|my record|puraana report|report.*dikhao|pichela record)",
            "app_info":          r"\b(aarogyaone|aarogya one|phr app|health app|ye app.*kya|app.*shu che|app.*ki hai)\b",
            "lab_reports":       r"(lab report|report|test report|casesheet|pending report|report.*kab.*milega|download.*report)",
            "emergency":         r"\b(emergency|urgent|serious|critical|chest pain|breath|ambulance|accident|khun|blood|heart attack)\b",
            "helpline":          r"\b(helpline|toll free|contact|phone|call|number|1800|1075|104|baat karni)\b",
            "thanks":            r"\b(thank|thanks|shukriya|dhanyawad|meherbani|dhanyavad|thnx|thx)\b",
        }

    def detect_language(self, text):
        t = text.lower()
        # Scoring keywords
        scores = {"gu": 0, "hi": 0, "pa": 0, "en": 0}
        
        # Unique/Strong keywords
        if re.search(r"\b(che|shu|kem|joiye|nathi|karvu|karo|ne)\b", t): scores["gu"] += 5
        if re.search(r"\b(hai|kya|kaise|karna|chaiye|hoga|kariye)\b", t): scores["hi"] += 3
        if re.search(r"\b(ki|kiven|kithe|duso|chahida|si|han)\b", t): scores["pa"] += 5
        
        # Generic check
        if re.search(r"\b(how|what|download|downloading|app|cert|get|give)\b", t): scores["en"] += 2
        
        best_lang = max(scores, key=scores.get)
        return best_lang if scores[best_lang] > 0 else "en"

    def detect_intent(self, text):
        t = text.lower().strip()
        found = []
        for intent, pattern in self.intents.items():
            if re.search(pattern, t, re.IGNORECASE):
                found.append(intent)
        return found if found else ["unknown"]

    def get_main_category(self, intents):
        """Extract main category from intents"""
        for intent in intents:
            if intent.startswith("abha"):
                return "abha"
            elif intent.startswith("ayushman"):
                return "ayushman"
            elif intent.startswith("covid"):
                return "covid"
            elif intent.startswith("app"):
                return "aarogyaone"
        return None

    def ask_subcategory(self, category, lang="en"):
        """Ask user to select a sub-category by typing what they want"""
        subcats = self.category_subcategories.get(category, {})
        
        if lang == "hi":
            msgs = {
                "abha": "ABHA कार्ड के बारे में आप क्या जानना चाहते हैं?",
                "ayushman": "Ayushman कार्ड के बारे में आप क्या जानना चाहते हैं?",
                "covid": "COVID के बारे में आप क्या जानना चाहते हैं?",
                "aarogyaone": "AarogyaOne ऐप के बारे में आप क्या जानना चाहते हैं?"
            }
        elif lang == "gu":
            msgs = {
                "abha": "ABHA કાર્ડ વિશે તમે શું જાણવા માંગો છો?",
                "ayushman": "Ayushman કાર્ડ વિશે તમે શું જાણવા માંગો છો?",
                "covid": "COVID વિશે તમે શું જાણવા માંગો છો?",
                "aarogyaone": "AarogyaOne ઍપ વિશે તમે શું જાણવા માંગો છો?"
            }
        else:  # English
            msgs = {
                "abha": "What would you like to know about ABHA Card?",
                "ayushman": "What would you like to know about Ayushman Card?",
                "covid": "What would you like to know about COVID Certificate?",
                "aarogyaone": "What would you like to know about AarogyaOne App?"
            }
        
        msg = msgs.get(category, "What would you like to know?")
        response = f"\n{DIV}\n  ❓  {msg}\n{DIV}\n\n"
        
        # Add options without numbers - just text
        for sub_key, sub_data in subcats.items():
            sub_label = sub_data.get(lang, sub_data.get("en", sub_key))
            response += f"  •  {sub_label}\n"
    
        
        self.pending_category = category
        return response

    def match_subcategory(self, user_input, category, lang="en"):
        """Match user input to a sub-category using keywords and natural language"""
        t = user_input.lower().strip()
        subcats = self.category_subcategories.get(category, {})
        
        # Enhanced keyword matching - check for multiple keywords per sub-category
        best_match = None
        best_score = 0
        
        for sub_key, sub_data in subcats.items():
            keywords = sub_data.get("keywords", "").lower()
            sub_label = sub_data.get(lang, sub_data.get("en", "")).lower()
            
            score = 0
            
            # Check keyword matches
            clean_keywords = keywords.replace(r'\b(', '').replace(r')\b', '')
            keyword_list = [k.strip() for k in clean_keywords.split('|') if k.strip()]
            for keyword in keyword_list:
                if keyword in t:
                    score += 2  # Keyword match gets high score
            
            # Check if sub-label words are in input
            label_words = [w.strip() for w in sub_label.split() if w.strip()]
            for word in label_words:
                if word in t:
                    score += 1  # Label word match gets lower score
            
            # Check for exact phrases
            if sub_label in t or any(phrase in t for phrase in [
                f"how to {sub_key}", f"{sub_key} steps", f"{sub_key} process"
            ]):
                score += 3  # Exact match gets highest score
            
            if score > best_score:
                best_score = score
                best_match = (sub_key, sub_data.get(lang, sub_data.get("en")))
        
        if best_score > 0:
            self.pending_category = None
            return best_match
        
        # No match found
        return None, None

    def get_rag_response(self, query, min_score=0.15, lang="en"):
        best, answers = self.rag.get_answer(query, top_k=2)
        if not answers or answers[0]["score"] < min_score:
            return None
        lines = [l.strip() for l in best.strip().split(". ") if l.strip()]
        
        ld = LANG_DATA.get(lang, LANG_DATA["en"])
        question = ld.get("satisfaction", "Do you have any other questions? (Yes / No)")
        
        return (
            f"\n{DIV}\n"
            f"  ℹ️   Information\n"
            f"{DIV}\n\n"
            + "\n".join(f"  •  {l}" for l in lines)
            + f"\n{DIV}\n\n"
            + f"  ❓  {question}\n"
        )

    def build_response(self, intents, user_input, lang="en"):
        responses = []
        ld = LANG_DATA.get(lang, LANG_DATA["en"])
        
        # Handle Greet - Show language selection only if no language selected yet
        if "greet" in intents:
            if self.selected_lang:
                # Language already selected - show language-specific greeting
                responses.append(
                    f"\n{DIV}\n"
                    f"  👋  {ld['greet']}\n"
                    f"{DIV}\n"
                    f"\n  {ld['ask_assist']}\n"
                    f"\n  {ld['help_list']}\n"
                    f"  •  ABHA Card\n"
                    f"  •  Ayushman Bharat\n"
                    f"  •  COVID Certificate\n"
                    f"  •  AarogyaOne App\n"
                    f"{DIV}\n"
                )
            else:
                # No language selected yet - show language selection screen
                responses.append(INITIAL_GREETING)
        
        # Priority: Emergency
        if "emergency" in intents:
            return (
                f"\n{'═' * 52}\n"
                f"  🚨  {ld['emergency']}\n"
                f"{'═' * 52}\n"
                f"\n  🚑  Ambulance      :  108  (Free, 24 x 7)\n"
                f"  🏥  Health Helpline :  104\n"
                f"  🆘  National Emerg  :  112\n"
                f"\n  ⚠️   {ld['emergency_warn']}\n"
                f"  ⚠️   {ld['emergency_call']}\n"
                f"{'═' * 52}\n"
            )

        processed_intents = set()
        for intent in intents:
            if intent in ["greet", "emergency", "unknown"] or intent in processed_intents:
                continue
            processed_intents.add(intent)

            if intent == "goodbye":
                responses.append(
                    f"\n{DIV}\n"
                    f"  👋  {ld['goodbye']}\n"
                    f"{DIV}\n"
                    f"\n  📱  Download AarogyaOne App:\n"
                    f"       {APP_LINK}\n"
                    f"\n  💚  {ld['stay_touch']}\n"
                    f"{DIV}\n"
                )

            elif intent == "thanks":
                responses.append(
                    f"\n{DIV}\n"
                    f"  😊  {ld['welcome']}\n"
                    f"{DIV}\n"
                    f"\n  •  {ld['anything_else']}\n"
                    f"  •  Download AarogyaOne for full records.\n"
                    f"\n  📱  {APP_LINK}\n"
                    f"{DIV}\n"
                )

            elif intent == "abha_info":
                # Only show summary if user EXPLICITLY asks for summary/info AND NOT for create/download
                if not ("abha_create" in intents or "abha_download" in intents):
                    # Check if user explicitly asked for summary/info
                    if re.search(r"\b(summary|info|information|details|vistar|jaankari|jankari|baare|vishay|माहिती|जानकारी|સારાંશ)\b", user_input, re.IGNORECASE):
                        if lang == "gu":
                            rows = ["ABHA એક 14-અંકનું ડિજિટલ આરોગ્ય ID છે", "તમામ આરોગ્ય રેકોર્ડ્સ એક જગ્યાએ સાચવવાં માટે", "નવું બનાવવું: 'Create ABHA' લખો", "'Download ABHA' લખીને ડાઉનલોડ કરો"]
                        elif lang == "hi":
                            rows = ["ABHA एक 14-अंकीय डिजिटल स्वास्थ्य ID है", "सभी चिकित्सा रिकॉर्ड एक जगह प्रबंधित करने के लिए", "नया बनाने के लिए: 'Create ABHA' लिखें", "डाउनलोड करने के लिए: 'Download ABHA' लिखें"]
                        else:
                            rows = ["ABHA is a 14-digit unique health ID for all Indians", "Store and share medical records digitally", "To Create: Type 'Create ABHA'", "To Download: Type 'Download ABHA'"]
                        responses.append(S(f"{ld['abha_name']} Summary", "🏥", rows=rows, lang=lang, card_helpline="abha"))

            elif intent == "abha_otp_issue":
                if lang == "gu":
                    rows = ["તમારો મોબાઇલ નંબર આધાર સાથે લિંક છે કે નહીં તે તપાસો", "મોબાઇલ નેટવર્ક અને SMS કવરેજ તપાસો", "થોડી વાર પછી પુનઃપ્રયાસ કરો (UIDAI સર્વર સમસ્યા)", "આધાર વેબસાઇટ પર મોબાઇલ નંબર ચકાસો"]
                    note = "જો સમસ્યા ચાલુ રહે, તો UIDAI ને 1947 પર કૉલ કરો."
                elif lang == "hi":
                    rows = ["जांचें कि आपका मोबाइल नंबर आधार से लिंक है या नहीं", "मोबाइल नेटवर्क और SMS कवरेज जांचें", "कुछ समय बाद दोबारा कोशिश करें (UIDAI सर्वर व्यस्त)", "आधार वेबसाइट पर मोबाइल नंबर सत्यापित करें"]
                    note = "यदि समस्या बनी रहे, तो UIDAI की हेल्पलाइन 1947 पर कॉल करें।"
                else:
                    rows = ["Check if your mobile number is linked to Aadhaar", "Check mobile network and SMS coverage", "Try again after some time (UIDAI server might be busy)", "Verify mobile number on Aadhaar website"]
                    note = "If issue persists, call UIDAI helpline at 1947."
                responses.append(S(f"{ld['abha_name']} {ld['otp_issue']}", "🔐", rows=rows, note=note, lang=lang, card_helpline="abha"))

            elif intent == "abha_other":
                if lang == "gu":
                    rows = [
                        "ખાતું પુનઃપ્રાપ્તિ, પ્રોફાઇલ અપડેટ અથવા તકનીકી સમસ્યાઓ માટે, abdm.gov.in ની મુલાકાત લો",
                        "તમે તમારી પ્રોફાઇલ માહિતી અપડેટ કરી શકો છો અથવા પાસવર્ડ બદલી શકો છો",
                        "ABDM હેલ્પલાઇન 1800-11-4477 નો સંપર્ક કરો",
                        "એપ્લિકેશન સંબંધિત સમસ્યાઓ માટે, Google Play Store પર અપડેટ્સ તપાસો"
                    ]
                elif lang == "hi":
                    rows = [
                        "खाता पुनर्प्राप्ति, प्रोफ़ाइल अपडेट या तकनीकी समस्याओं के लिए, abdm.gov.in पर जाएं",
                        "आप अपनी प्रोफ़ाइल जानकारी अपडेट कर सकते हैं या पासवर्ड रीसेट कर सकते हैं",
                        "सहायता के लिए ABDM हेल्पलाइन 1800-11-4477 पर संपर्क करें",
                        "ऐप से जुड़ी समस्याओं के लिए, Google Play Store पर अपडेट जांचें"
                    ]
                else:
                    rows = [
                        "For account recovery, profile updates, or technical problems, visit abdm.gov.in",
                        "You can update your profile, change mobile number, or reset your password",
                        "Contact the ABDM helpline at 1800-11-4477 for direct assistance",
                        "For AarogyaOne app issues, please ensure you have the latest update from Play Store"
                    ]
                responses.append(S(f"Other {ld['abha_name']} Issues", "🛠️", rows=rows, lang=lang, card_helpline="abha"))

            elif intent == "ayushman_get":
                if lang == "gu":
                    rows = [
                        "pmjay.gov.in પર તમારી પાત્રતા તપાસો",
                        "મોબાઇલ નંબર અને OTP દાખલ કરીને ચકાસો",
                        "નજીકના CSC સેન્ટર અથવા Ayushman Mitra ની મુલાકાત લો",
                        "આધાર કાર્ડ અને રેશન કાર્ડ સાથે લાવો",
                        "બાયોમેટ્રિક ચકાસણી કરવામાં આવશે",
                        "તમારું Ayushman ગોલ્ડન કાર્ડ ત્યાં જ અથવા થોડા દિવસોમાં મળશે"
                    ]
                elif lang == "hi":
                    rows = [
                        "pmjay.gov.in पर अपनी पात्रता जांचें",
                        "मोबाइल नंबर और OTP दर्ज करके सत्यापित करें",
                        "निकटतम CSC सेंटर या Ayushman Mitra से मिलें",
                        "आधार कार्ड और राशन कार्ड साथ लाएं",
                        "बायोमेट्रिक सत्यापन किया जाएगा",
                        "आपका Ayushman कारड कुछ दिनों में मिल जऻeएगा",
                        "1500+ સારવાર પદ્ધતિઓ અને શસ્ત્રક્રિયાઓ કવર કરે છે",
                        "હોસ્પિટલમાં દાખલ થવાના 3 દિવસ પહેલા અને 15 દિવસ પછીનો ખર્ચ કવર થાય છે",
                        "પહેલેથી હોય તેવી તમામ બીમારીઓ પહેલા દિવસથી કવર થાય છે",
                        "ભારતમાં 25,000+ અનુમતિ પ્રાપ્ત હોસ્પિટલોમાં કેશલેસ સારવાર",
                        "ICU ચાર્જ, દવાઓ, શસ્ત્રક્રિયા, ડાયગ્નોસ્ટિક ટેસ્ટ કવર કરે છે",
                        "સરકારી અને ખાનગી બંને હોસ્પિટલોમાં માન્ય છે"
                    ]
                elif lang == "hi":
                    rows = [
                        "PMJAY (आयुष्मान भारत) कार्ड प्रति परिवार प्रति वर्ष ₹5 लाख तक स्वास्थ्य बीमा देता है",
                        "1500+ उपचार प्रक्रियाएं और सर्जरी कवर करता है",
                        "अस्पताल में भर्ती होने से 3 दिन पहले और 15 दिन बाद तक का खर्च कवर है",
                        "सभी पहले से मौजूद बीमारियां पहले दिन से कवर होती हैं",
                        "भारत में 25,000+ अनुमोदित अस्पतालों में कैशलेस इलाज",
                        "ICU चार्ज, दवाइयां, सर्जरी, डायग्नोस्टिक टेस्ट कवर हैं",
                        "सरकारी और प्राइवेट दोनों अस्पतालों में मान्य है"
                    ]
                else:
                    rows = [
                        "PMJAY (Ayushman Bharat) card covers Rs 5 Lakh health insurance per family per year",
                        "Covers over 1500 treatment procedures and surgeries",
                        "Coverage includes pre-hospitalization (3 days) and post-hospitalization (15 days)",
                        "Covers all pre-existing diseases from day one",
                        "Cashless treatment at 25,000+ empanelled hospitals across India",
                        "Covers ICU charges, medicines, surgery, and diagnostic tests",
                        "Valid at both government and private hospitals"
                    ]
                responses.append(S(f"PMJAY / {ld['ayushman_name']} Benefits & Coverage", "🥇", rows=rows, lang=lang, card_helpline="ayushman"))

            elif intent == "ayushman_info":
                if not ("ayushman_download" in intents or "ayushman_coverage" in intents):
                    # Check if user explicitly asked for summary/info
                    if re.search(r"\b(summary|info|information|details|vistar|jaankari|jankari|baare|vishay|माहिती|जानकारी|સારાંશ)\b", user_input, re.IGNORECASE):
                        if lang == "gu":
                            rows = ["વર્ષિક ₹5 લાખ સુધી મુક્ત સ્વાસ્થ્ય કવર", "તમામ મોટી બીમારીઓ અને શસ્ત્રક્રિયા કવર કરે છે", "25,000+ અનુમતિ પ્રાપ્ત હોસ્પિટલોમાં કેશલેસ સુવિધા", "ડાઉનલોડ કરવા માટે: 'Download Ayushman' લખો"]
                        elif lang == "hi":
                            rows = ["सालाना ₹5 लाख तक मुफ्त स्वास्थ्य कवर", "सभी बड़ी बीमारियों और सर्जरी को कवर करता है", "25,000+ अनुमोदित अस्पतालों में कैशलेस सुविधा", "डाउनलोड के लिए: 'Download Ayushman' लिखें"]
                        else:
                            rows = ["Rs 5 Lakh free health cover per family per year", "Covers major surgeries and hospital treatments", "Cashless at 25,000+ empanelled hospitals", "To Download: Type 'Download Ayushman'"]
                        responses.append(S(f"{ld['ayushman_name']} Summary", "🥇", rows=rows, lang=lang, card_helpline="ayushman"))

            elif intent == "abha_otp_issue":
                if lang == "gu":
                    rows = ["તમારો મોબાઇલ નંબર આધાર સાથે લિંક છે કે નહીં તેය તપાસો", "મોબાઇલ નેટવર્ક અને SMS કવરેજ તપાસો", "થોડી વર સુધી પછી પુનઃપ્રયાસ કરો (UIDAI સર્વર સમસ્યા)", "આધાર વેબસાઇટ પર મોબાઇલ નંબર ચકાસો"]
                    note = "જો સમસ્યા ચાલુ રહે, તો UIDAI ને 1947 પર કૉલ કરો."
                elif lang == "hi":
                    rows = ["जांचें कि आपका मोबाइल नंबर आधार से लिंक है या नहीं", "मोबाइल नेटवर्क और SMS कवरेज जांचें", "कुछ समय बाद दोबारा कोशिश करें (UIDAI सर्वर व्यस्त)", "आधार वेबसाइट पर मोबाइल नंबर सत्यापित करें"]
                    note = "यदि समस्या बनी रहे, तो UIDAI की हेल्पलाइन 1947 पर कॉल करें।"
                else:
                    rows = ["Ensure your mobile number is linked with Aadhaar", "Check mobile network and SMS storage", "Retry after some time (UIDAI server busy)", "Verify mobile number on Aadhaar portal"]
                    note = "If issue persists, contact UIDAI helpline 1947."
                responses.append(S(ld['otp_issue'], "🔑", rows=rows, note=note, lang=lang, card_helpline="abha"))

            elif intent == "lab_reports":
                if lang == "gu":
                    rows = ["AarogyaOne ઍપમાં 'Pull Records' વિકલ્પ ખોલો", "ત્યાં તમને લંબિત દસ્તાવેજો દેખાશે", "હોસ્પિટલ રેકોર્ડ્સ લિંક કરવા માટે ABHA ઉપયોગ કરો", "રેકોર્ડ્સ ત્યારે દેખાય છે જ્યારે હોસ્પિટલ/લેબ તેમને ડિજિટલલી શેર કરે"]
                    note = "તમે દસ્તાવેજોને જાતે પણ અપલોડ કરી શકો છો."
                elif lang == "hi":
                    rows = ["AarogyaOne ऐप में 'Pull Records' विकल्प खोलें", "वहां आपको लंबित दस्तावेज़ दिखाई देंगे", "हॉस्पिटल रिकॉर्ड लिंक करने के लिए ABHA का उपयोग करें", "रिकॉर्ड तब दिखाई देते हैं जब अस्पताल/लैब उन्हें डिजिटल रूप से साझा करता है"]
                    note = "आप दस्तावेजों को स्वयं भी अपलोड कर सकते हैं।"
                else:
                    rows = ["Go to 'Pull Records' in AarogyaOne App", "Check if any documents are pending under your ABHA", "Ensure ABHA is correctly linked in the app", "Records show up only when hospital/lab pushes them to ABHA"]
                    note = "You can manually upload documents/reports to the records section."
                responses.append(S(ld['lab_report'], "📊", rows=rows, note=note, lang=lang, card_helpline="aarogyaone"))

            elif intent == "ayushman_info":
                if not ("ayushman_download" in intents):
                    if lang == "gu":
                        rows = ["વર્ષિક ₹5 લાખ સુધી મુક્ત સ્વાસ્થ્य કવર", "તમામ મોટી બીમારીઓ અને શસ્ત્રક્રિયા કવર કરે છે", "25,000+ અનુમતિ પ્રાપ્ત હોસ્પિટલોમાં કેશલેસ સુવિધા", "ડાઉનલોડ કરવા માટે: 'Download Ayushman' લખો"]
                    elif lang == "hi":
                        rows = ["सालाना ₹5 लाख तक मुफ्त स्वास्थ्य कवर", "सभी बड़ी बीमारियों और सर्जरी को कवर करता है", "25,000+ अनुमोदित अस्पतालों में कैशलेस सुविधा", "डाउनलोड के लिए: 'Download Ayushman' लिखें"]
                    else:
                        rows = ["Rs 5 Lakh free health cover per family per year", "Covers major surgeries and hospital treatments", "Cashless at 25,000+ empanelled hospitals", "To Download: Type 'Download Ayushman'"]
                    responses.append(S(f"{ld['ayushman_name']} Summary", "🥇", rows=rows, lang=lang, card_helpline="ayushman"))

            elif intent == "covid_info":
                if not ("covid_download" in intents):
                    # Show COVID sub-category menu instead of summary
                    # This routes to the ask_subcategory flow so user picks what they need
                    return self.ask_subcategory("covid", lang)

            elif intent == "app_info":
                if lang == "gu":
                    rows = ["તમારા આરોગ્ય રેકોર્ડ્સ સંચાલિત કરવાની મુક્ત ઍપ", "દસ્તાવેજોને સુરક્ષિત રીતે અપલોડ અને શેર કરો", "ફોનમાંથી ડૉક્ટર નિયુક્તિ બુક કરો", "તમારા તબીબી ઇતિહાસ સિંક કરવા માટે ABHA કનેક્ટ કરો"]
                elif lang == "hi":
                    rows = ["आपके ব्যक्તिगत स्वास्थ्य रिकॉर्ड प्रबंधित करने के लिए मुफ्त ऐप", "दस्तावेजों को सुरक्षित रूप से अपलोड और साझा करें", "फोन से डॉक्टर नियुक्ति बुक करें", "अपने चिकित्सा इतिहास को सिंक करने के लिए ABHA कनेक्ट करें"]
                else:
                    rows = ["Free app to manage your personal health records", "Upload and share documents securely", "Book doctor appointments from phone", "Link ABHA to sync your medical history"]
                responses.append(S(f"Summary: {ld['app_name']}", "📱", rows=rows, lang=lang, card_helpline="aarogyaone"))

            elif intent == "app_appointment":
                if lang == "gu":
                    rows = ["AarogyaOne PHR ઍપ તમારા ફોન પર ખોલો", "હોમ પેજ પર Doctor સેક્શન જાઓ", "ડૉક્ટરનું નામ અને વિશેષતા દ્વારા શોધો", "તમારો પસંદીદા ડૉક્ટર શોધીને Book Consultation ક્લિક કરો", "નિયુક્તિ માટે સુવિધાજનક તારીખ અને સમયનો સ્લોટ પસંદ કરો", "પરિવાર સભ્য માટે નિયુક્તિ બુક કરવા માટે પેશેન્ટ પ્રોફાઈલ બદલી શકો છો", "નિયુક્તિ વિગતોની પુષ્ટિ કરો અને તમારા રજિસ્ટર્ડ મોબાઈલ નંબર પર પુષ્ટિ પ્રાપ્ત કરો", "ઍપમાંથી તમામ નિયુક્તિઓ જોઈ અને સંચાલિત કરી શકો છો"]
                elif lang == "hi":
                    rows = ["AarogyaOne PHR ऐप अपने फोन पर खोलें", "होम पेज पर Doctor सेक्शन जाएं", "डॉक्टर का नाम और विशेषता से खोजें", "अपना पसंदीदा डॉक्टर खोजकर Book Consultation पर क्लिक करें", "नियुक्ति के लिए सुविधाजनक तारीख और समय स्लोट चुनें", "परिवार के सदस्य की नियुक्ति बुक करने के लिए रोगी प्रोफाइल बदल सकते हैं", "नियुक्ति विवरण की पुष्टि करें और अपने पंजीकृत मोबाइल नंबर पर पुष्टि प्राप्त करें", "ऐप से सभी नियुक्तियों को देख और प्रबंधित कर सकते हैं"]
                else:
                    rows = ["Open AarogyaOne PHR app on your phone", "Go to Doctor section available at the home page", "Search for doctors by doctor name and specialization", "Click on book consultation once you find your preferred doctor", "Choose your convenient date and time slot for the appointment", "You can also change the patient profile to book an appointment for your family member", "Confirm your appointment details and receive confirmation on your registered mobile number", "You can view and manage all your appointments from the app"]
                responses.append(S(f"{ld['app_name']} Appointment", "📅", rows=rows, lang=lang, card_helpline="aarogyaone"))

            elif intent == "app_link_abha":
                # Full step-by-step ABHA linking flow with AarogyaOne
                if lang == "gu":
                    rows = [
                        "AarogyaOne ઍપ ખોલો અને આધાર કાર્ડ અથવા મોબાઇલ નંબરથી લૉગિન કરો",
                        "તમારા રજિસ્ટર્ડ મોબાઇલ નંબર પર મોકલેલ OTP દાખલ કરો",
                        "જો આધાર કાર્ડ વાપર્યું હોય, તો ચકાસણી માટે મોબાઇલ નંબર દાખલ કરો",
                        "તમારી વિગતો (નામ, જન્મ તારીખ, સરનામું) તપાસો",
                        "જો બધી વિગતો સાચી હોય, તો Continue ક્લિક કરો",
                        "✅ તમારું ABHA સફળતાપૂર્વક AarogyaOne ઍપ સાથે લિંક થઈ ગયું!",
                        "📄 દસ્તાવેજ ABHA સાથે લિંક કરવા: Records સેક્શનમાં જાઓ → દસ્તાવેજ અપલોડ કરો → 'Link with ABHA' બટન ક્લિક કરો",
                        "✅ તમારો દસ્તાવેજ સફળતાપૂર્વક ABHA સાથે લિંક થઈ ગયો!"
                    ]
                elif lang == "hi":
                    rows = [
                        "AarogyaOne ऐप खोलें और आधार कार्ड या मोबाइल नंबर से लॉगिन करें",
                        "आपके रजिस्टर्ड मोबाइल नंबर पर भेजे गए OTP दर्ज करें",
                        "अगर आधार कार्ड से लॉगिन किया है, तो वेरिफिकेशन के लिए मोबाइल नंबर दर्ज करें",
                        "अपनी डिटेल्स (नाम, जन्म तिथि, पता) चेक करें",
                        "अगर सब डिटेल्स सही हैं, तो Continue पर क्लिक करें",
                        "✅ आपका ABHA सफलतापूर्वक AarogyaOne ऐप से लिंक हो गया!",
                        "📄 डॉक्यूमेंट ABHA से लिंक करने के लिए: Records सेक्शन में जाएं → डॉक्यूमेंट अपलोड करें → 'Link with ABHA' बटन पर क्लिक करें",
                        "✅ आपका डॉक्यूमेंट सफलतापूर्वक ABHA से लिंक हो गया!"
                    ]
                else:
                    rows = [
                        "Open the AarogyaOne app and login with your Aadhaar Card or Mobile Number",
                        "Enter the OTP sent to your registered mobile number",
                        "If you used Aadhaar Card, enter your mobile number for verification",
                        "Check your details (Name, Date of Birth, Address) on screen",
                        "If all details are correct, click Continue",
                        "✅ Your ABHA is successfully created and linked with the AarogyaOne app!",
                        "📄 To link documents with ABHA: Go to Records section → Upload your document → Click 'Link with ABHA' button",
                        "✅ Your document is successfully linked with ABHA!"
                    ]
                responses.append(S(f"Link ABHA with {ld['app_name']}", "🔗", rows=rows, lang=lang, card_helpline="aarogyaone"))

            elif intent == "abha_download":
                if lang == "gu":
                    rows = ["abdm.gov.in ખોલો", "'Download ABHA Card' ક્લિક કરો", "મોબાઇલ નંબર દાખલ કરો", "OTP સાથે ચકાસો", "કાર્ડ PDF તરીકે ડાઉનલોડ થાય છે"]
                elif lang == "hi":
                    rows = ["abdm.gov.in ખોलें", "'Download ABHA Card' क्लिक करें", "मोबाइल नंबर डालें", "OTP से सत्यापित करें", "कार्ड PDF के रूप में डाउनलोड होता है"]
                else:
                    rows = ["Visit abdm.gov.in", "Click 'Download ABHA Card'", "Enter mobile number", "Verify with OTP", "Card downloads as PDF"]
                responses.append(S(f"{ld['abha_name']} Download", "📥", rows=rows, lang=lang, card_helpline="abha"))

            elif intent == "abha_create":
                if lang == "gu":
                    rows = ["abdm.gov.in ખોલો", "'Create ABHA' ક્લિક કરો", "આધાર નંબર દાખલ કરો", "OTP સાથે ચકાસો", "વિવરણ ભરીને PDF ડાઉનલોડ કરો"]
                elif lang == "hi":
                    rows = ["abdm.gov.in खोलें", "'Create ABHA' क्लिक करें", "आधार नंबर दर्ज करें", "OTP से सत्यापित करें", "विवरण भरकर PDF डाउनलोड करें"]
                else:
                    rows = ["Visit abdm.gov.in", "Click 'Create ABHA'", "Enter Aadhaar number", "Verify with OTP", "Fill details and download PDF"]
                responses.append(S(f"{ld['abha_name']} Create", "📝", rows=rows, lang=lang, card_helpline="abha"))

            elif intent == "covid_download":
                # Clarify that COVID certificates are only for download, not creation
                is_create_query = re.search(r"\b(create|bana|register|make|new|nava|naya)\b", user_input.lower())
                
                if lang == "gu":
                    rows = ["www.cowin.gov.in ખોલો", "'Register/Sign In' ક્લિક કરો", "મોબાઇલ નંબર દાખલ કરો", "OTP સાથે લૉગ ઇન કરો", "પ્રમાણપત્ર ડાઉનલોડ કરો"]
                    title = f"{ld['covid_name']} Download"
                    note = "નોંધ: COVID પ્રમાણપત્ર બનાવી શકાતું નથી, માત્ર ડાઉનલોડ કરી શકાય છે." if is_create_query else None
                elif lang == "hi":
                    rows = ["www.cowin.gov.in खोलें", "'Register/Sign In' क्लिक करें", "मोबाइल नंबर दर्ज करें", "OTP से लॉगिन करें", "प्रमाणपत्र डाउनलोड करें"]
                    title = f"{ld['covid_name']} Download"
                    note = "नोट: COVID प्रमाणपत्र बनाया नहीं जा सकता, केवल डाउनलोड किया जा सकता है।" if is_create_query else None
                else:
                    rows = ["Visit www.cowin.gov.in", "Click 'Register/Sign In'", "Enter mobile number", "Verify with OTP", "Download Certificate"]
                    title = f"{ld['covid_name']} Download"
                    note = "Note: COVID certificates cannot be created, only downloaded." if is_create_query else None
                
                responses.append(S(title, "💉", rows=rows, note=note, lang=lang, card_helpline="covid"))

            elif intent == "app_not_working":
                responses.append(
                    f"\n⚠️ **{ld['app_name']} Issue?**\n"
                    f"\n**{ld['fix_steps']}**\n"
                    f"  1. Force close and reopen the app\n"
                    f"  2. Check your internet connection\n"
                    f"  3. Update app from Google Play Store\n"
                    f"  4. Clear app cache in phone settings\n"
                    f"  5. Reinstall if problem continues\n"
                    f"\n**{ld['still_not_working']}**"
                    f"{helpline_box('aarogyaone', lang)}"
                )

            elif intent == "helpline":
                responses.append(
                    f"\n📞 **India Health Helplines**\n"
                    f"\n• **Ambulance**: 108\n"
                    f"• **Health Helpline**: 104\n"
                    f"• **CoWIN / COVID**: 1075\n"
                    f"• **Ayushman Bharat**: 14555\n"
                    f"• **ABHA / ABDM**: 1800-11-4477\n"
                )

        # Ensure we always return a valid response if no specific intent was handled
        if not responses:
            rag = self.get_rag_response(user_input, lang=lang)
            if rag:
                return rag
            return out_of_scope(user_input, lang)

        return "\n".join(responses)

    def handle_feedback(self, text, lang="en"):
        """Handle simple user feedback (yes/no/satisfied) in English, Hindi, and Gujarati.
        Only triggers on PURE feedback — if the message contains a real question/intent, skip feedback."""
        t = text.lower().strip()
        
        # If the input contains a real question intent, don't treat it as feedback
        # This allows users to ask new questions without saying Yes/No first
        real_intents = self.detect_intent(text)
        real_intents_filtered = [i for i in real_intents if i not in ("greet", "thanks", "goodbye", "unknown")]
        if real_intents_filtered:
            return None  # Let the normal chat flow handle it
        
        # YES / I have more questions
        yes_pattern = r"^(yes|yep|yeah|sure|y|haa|haan|ha|jee|ji|ho|ha bhai|yes please)\b"
        if re.search(yes_pattern, t, re.IGNORECASE):
            ld = LANG_DATA.get(lang, LANG_DATA["en"])
            return (
                f"\n{DIV}\n"
                f"  👋  {ld['greet']}\n"
                f"{DIV}\n"
                f"\n  {ld['ask_assist']}\n"
                f"\n  {ld['help_list']}\n"
                f"  •  ABHA Card\n"
                f"  •  Ayushman Bharat\n"
                f"  •  COVID Certificate\n"
                f"  •  AarogyaOne App\n"
                f"{DIV}\n"
            )

        # NO / No more questions -> Goodbye
        no_pattern = r"^(no|nope|nah|not|na|naa|nahi|naahi|noo|ന|ना|नहीं|ના|નથી)\b"
        if re.search(no_pattern, t, re.IGNORECASE):
            ld = LANG_DATA.get(lang, LANG_DATA["en"])
            return (
                f"\n{DIV}\n"
                f"  👋  {ld['goodbye']}\n"
                f"{DIV}\n"
                f"\n  📱  Download AarogyaOne App:\n"
                f"       {APP_LINK}\n"
                f"\n  💚  {ld['stay_touch']}\n"
                f"{DIV}\n"
            )

        # POSITIVE FEEDBACK - Multiple variations (Thanks, okay, etc)
        positive_pattern = r"\b(okay|ok|good|great|awesome|perfect|excellent|satisfied|happy|liked|thanks|thank you|thank|" \
                          r"bilkul|bilkull|accha|achha|theek|hai|badhiya|shukriya|shukrya|dhanyavaad|" \
                          r"badiya|thaik|thik|" \
                          r"ठीक|बहुत सारा|शानदार|बेहतरीन|अच्छा|पसंद|आया|धन्यवाद|शुक्रिया|सही|" \
                          r"ઠીક|બહુ|સારું|શાનદાર|આભાર|સુક્રિया|બરોબર)\b"
        
        if re.search(positive_pattern, t, re.IGNORECASE):
            if lang == "hi":
                return "\n😊 **शुक्रिया! मुझे खुशी है कि मदद हो सकी।** \n\nक्या आपका कोई और सवाल है? (Yes/No)"
            elif lang == "gu":
                return "\n😊 **આભાર! મને આનંદ છે કે મદદ મળી।** \n\nશું તમારો કોઈ અન્ય પ્રશ્ન છે? (Yes/No)"
            else:
                return "\n😊 **Thank you! I'm glad I could help.** \n\nDo you have any other questions? (Yes/No)"
        
        # NEGATIVE FEEDBACK - Multiple variations
        negative_pattern = r"\b(bad|poor|not-satisfied|not-helpful|dissatisfied|terrible|awful|don't like|didn't help|" \
                          r"khrab|bura|bilkul nahi|bilkull nahi|kharab|" \
                          r"खराब|बुरा|संतुष्ट नहीं|मदद नहीं|पसंद नहीं|भयानक|" \
                          r"બુરું|ખરાબ|સंतुष्ट નથી|મદદ નથી|પસંદ નથી)\b"
        
        if re.search(negative_pattern, t, re.IGNORECASE):
            if lang == "hi":
                return "\n😔 **मुझे खेद है। कृपया support@aarogyaone.in पर ईमेल करें या 1800-11-4477 पर कॉल करें।**"
            elif lang == "gu":
                return "\n😔 **મને અફસોસ છે। કૃપया support@aarogyaone.in પર ઈમેલ કરો અથવા 1800-11-4477 પર કૉલ કરો।**"
            else:
                return "\n😔 **I'm sorry. Please email support@aarogyaone.in or call 1800-11-4477.**"
        
        return None
    
    def chat(self, user_input):
        user_input = user_input.strip()
        if not user_input:
            return f"\n🤔 Type a message."

        # Handle explicit language selection by number (1, 2, or 3)
        if user_input in ["1", "2", "3"] and not self.pending_category:
            lang_map = {"1": "en", "2": "hi", "3": "gu"}
            self.selected_lang = lang_map[user_input]
            confirmations = {
                "en": "Language set to English! How can I assist you today?",
                "hi": "भाषा हिंदी सेट की गई है! मैं आज आपकी कैसे मदद कर सकता हूँ?",
                "gu": "ભાષા ગુજરાતી સેટ કરવામાં આવી છે! હું આજે તમને કેવી રીતે મદદ કરી શકું?"
            }
            return f"\n✅ **{confirmations[self.selected_lang]}**"
        
        # Handle language selection by name (English, Hindi, Gujarati)
        lang_name = user_input.lower().strip()
        if not self.pending_category and re.search(r"\b(english|angreezi)\b", lang_name):
            self.selected_lang = "en"
            return f"\n✅ **Language set to English! How can I assist you today?**"
        elif not self.pending_category and re.search(r"\b(hindi|hindee|hindi bhasha)\b", lang_name):
            self.selected_lang = "hi"
            return f"\n✅ **भाषा हिंदी सेट की गई है! मैं आज आपकी कैसे मदद कर सकता हूँ?**"
        elif not self.pending_category and re.search(r"\b(gujarati|gujarathi|gujarata)\b", lang_name):
            self.selected_lang = "gu"
            return f"\n✅ **ભાષા ગુજરાતી સેટ કરવામાં આવી છે! હું આજે તમને કેવી રીતે મદદ કરી શકું?**"

        # Use persistent language if selected, else DEFAULT TO ENGLISH
        if self.selected_lang:
            lang = self.selected_lang
        else:
            # DEFAULT TO ENGLISH if no language selected yet
            lang = "en"
        
        # ╔════════════════════════════════════════════════════════════╗
        # ║  CHECK IF THIS IS FEEDBACK (Yes/No/Thanks/etc)            ║
        # ╚════════════════════════════════════════════════════════════╝
        feedback_response = self.handle_feedback(user_input, lang)
        if feedback_response:
            self.pending_category = None  # Clear any pending menu
            return feedback_response

        # ╔════════════════════════════════════════════════════════════╗
        # ║  HANDLE PENDING SUB-CATEGORY SELECTION                    ║
        # ╚════════════════════════════════════════════════════════════╝
        if self.pending_category:
            # Check if user is trying to switch to a different main topic
            temp_intents = self.detect_intent(user_input)
            new_main = self.get_main_category(temp_intents)
            
            # If a new main category is detected and it's different, clear the pending state
            if new_main and new_main != self.pending_category:
                self.pending_category = None
            else:
                saved_category = self.pending_category  # Save before match clears it
                sub_key, sub_label = self.match_subcategory(user_input, saved_category, lang)
                
                if sub_key:
                    # Found a matching sub-category
                    # Map sub-category keys to their direct intent names
                    intent_map = {
                        "ayushman": {"coverage": "ayushman_coverage", "download": "ayushman_download", "get": "ayushman_get"},
                        "abha": {"create": "abha_create", "download": "abha_download", "otp_issue": "abha_otp_issue", "other": "abha_other"},
                        "covid": {"download": "covid_download"},
                        "aarogyaone": {"download": "app_download", "upload": "app_upload", "appointment": "app_appointment", "link_abha": "app_link_abha"},
                    }
                    
                    # Check if this sub-category has a direct intent handler
                    mapped_intent = intent_map.get(saved_category, {}).get(sub_key)
                    if mapped_intent:
                        self.pending_category = None
                        return self.build_response([mapped_intent], user_input, lang)
                    
                    # Fallback to RAG for sub-categories without a direct handler
                    subcats = self.category_subcategories.get(self.pending_category, {})
                    en_label = subcats.get(sub_key, {}).get("en", sub_label)
                    rag_query = f"{self.pending_category} {en_label}"
                    rag_response = self.get_rag_response(rag_query, lang=lang)
                    
                    if rag_response:
                        self.pending_category = None
                        return rag_response
                    else:
                        # No answer found in RAG
                        self.pending_category = None
                        error_msgs = {
                            "en": f"Sorry, I couldn't find specific information about '{sub_label}'. Please try rephrasing your question.",
                            "hi": f"माफ कीजिए, मुझे '{sub_label}' के बारे में विशिष्ट जानकारी नहीं मिली। कृपया अपना सवाल दोबारा लिखें।",
                            "gu": f"માફ કરો, મને '{sub_label}' વિશે જાનકારી મળી નહીં. કૃપયા તમારો પ્રશ્ન ફરીથી લખો."
                        }
                        return f"\n❌ {error_msgs.get(lang, error_msgs['en'])}"
                else:
                    # Check if it was a greeting or other basic intent - if so, clear pending
                    if any(i in ["greet", "thanks", "goodbye", "emergency"] for i in temp_intents):
                        self.pending_category = None
                    else:
                        # No matching sub-category - ask again
                        error_msgs = {
                            "en": "Sorry, I didn't understand. Please check the options below and try again.",
                            "hi": "माफ कीजिए, मुझे समझ नहीं आया। कृपया नीचे दिए गए विकल्पों की जांच करें और पुनः प्रयास करें।",
                            "gu": "માફ કરો, મને સમજ આવતું નથી. કૃપયા નીચેના વિકલ્પો તપાસો અને ફરી પ્રયાસ કરો."
                        }
                        return f"\n❓ {error_msgs.get(lang, error_msgs['en'])}\n\n" + self.ask_subcategory(self.pending_category, lang)
        
        
        self.conversation_history.append({"role": "user", "text": user_input, "lang": lang})
        
        intents = self.detect_intent(user_input)
        
        # ╔════════════════════════════════════════════════════════════╗
        # ║  CHECK IF USER IS ASKING GENERAL CATEGORY (NO SUB-INTENT) ║
        # ╚════════════════════════════════════════════════════════════╝
        main_category = self.get_main_category(intents)
        
        # Check for SPECIFIC action intents
        action_intents = [
            "abha_create", "abha_download", "abha_otp_issue", "abha_other",
            "ayushman_get", "ayushman_download", "ayushman_coverage",
            "abha_other",
            "covid_download",
            "app_download", "app_upload", "app_appointment", "app_link_abha", "app_share", "app_view"
        ]
        has_specific_action = any(intent in action_intents for intent in intents)
        
        # Check if input is very simple (just "category card" or "category")
        simple_input = len(user_input.split()) <= 2 and (
            re.search(r"\b(card|app|certificate)\b", user_input, re.IGNORECASE)
        )
        
        # If main category detected but no clear action intent, ask for sub-category
        if main_category and not has_specific_action and (simple_input or (
            "abha_info" in intents or "ayushman_info" in intents or 
            "covid_info" in intents or "app_info" in intents
        )):
            return self.ask_subcategory(main_category, lang)
        
        # FINAL FALLBACK: Build the response for the detected intents
        return self.build_response(intents, user_input, lang)
        


if __name__ == "__main__":
    bot = AarogyaChatbot()
    print("\n" + "="*52)
    print("      🏥  AarogyaOne Medical AI Chatbot")
    print("="*52)
    print("Welcome! Type 'exit' to quit.")
    print(bot.chat("hello"))

    while True:
        try:
            user_msg = input("\nYou: ").strip()
            if user_msg.lower() in ["exit", "quit", "bye"]:
                print(bot.chat("bye"))
                break
            if not user_msg: continue
            print(bot.chat(user_msg))
        except KeyboardInterrupt:
            print("\nGoodbye!"); break
        except Exception as e:
            print(f"\nAn error occurred: {e}")
