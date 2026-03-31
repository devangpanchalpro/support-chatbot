import re
from RAG_engine import RAGEngine


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
DIV      = "─" * 52

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
    },
    "hi": {
        "info": "Jaankari", "steps": "Steps", "note": "Note", "link": "Link", "helpline": "HELPLINE",
        "toll_free": "Toll-Free", "website": "Website", "hours": "Samay", "email": "Email",
        "greet": "Namaste! AarogyaOne mein aapka swagat hai", "help_list": "Main in cheezon mein madad kar sakta hoon:",
        "ask_assist": "Main aapki kaise madad kar sakta hoon?", "goodbye": "Dhanyawad! Swasth rahein!",
        "stay_touch": "Phir milenge. Apna khayal rakhein!", "welcome": "Aapka swagat hai!",
        "anything_else": "Kya main kisi aur cheez mein madad karoon?", "emergency": "EMERGENCY — TURANT CALL KAREIN!",
        "emergency_warn": "Emergency mein chatbot ka use mat karein!", "emergency_call": "Abhi 108 par call karein!",
        "fix_steps": "Quick Fix Steps:", "still_not_working": "Abhi bhi kaam nahi kar raha? Support ko call karein:",
        "abha_name": "ABHA Card", "ayushman_name": "Ayushman Card", "covid_name": "COVID Certificate",
        "app_name": "AarogyaOne App", "medical_name": "Medical Queries",
    },
    "gu": {
        "info": "Mahiti", "steps": "Steps", "note": "Note", "link": "Link", "helpline": "HELPLINE",
        "toll_free": "Toll-Free", "website": "Website", "hours": "Samay", "email": "Email",
        "greet": "Namaste! AarogyaOne ma tamaru swagat che", "help_list": "Hu aa badhi vastu ma madad kari saku chu:",
        "ask_assist": "Hu tamari kem madad kari saku?", "goodbye": "Aabhar! Swasth raho!",
        "stay_touch": "Aavjo. Tamaru dhyan rakhjo!", "welcome": "Tamaru swagat che!",
        "anything_else": "Bijri koi madad joiye che?", "emergency": "EMERGENCY — TURANT CALL KARO!",
        "emergency_warn": "Emergency ma chatbot no upyog na karo!", "emergency_call": "Hajis 108 par call karo!",
        "fix_steps": "Quick Fix Steps:", "still_not_working": "Hajju kaam nathi kartu? Support ne call karo:",
        "abha_name": "ABHA Card", "ayushman_name": "Ayushman Card", "covid_name": "COVID Certificate",
        "app_name": "AarogyaOne App", "medical_name": "Medical Queries",
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
        "app_name": "AarogyaOne App", "medical_name": "Medical Queries",
    }
}


def helpline_box(card_type, lang="en"):
    """Return a neat helpline block for the given card type"""
    h = HELPLINES.get(card_type, HELPLINES["abha"])
    ld = LANG_DATA.get(lang, LANG_DATA["en"])
    return (
        f"\n  ┌{'─'*46}┐\n"
        f"  │  📞  {ld['helpline']}: {h['name']:<28}│\n"
        f"  ├{'─'*46}┤\n"
        f"  │  ☎  {ld['toll_free']} : {h['number']:<27}│\n"
        f"  │  🌐  {ld['website']}  : {h['website']:<27}│\n"
        f"  │  🕐  {ld['hours']}    : {h['hours']:<27}│\n"
        f"  │  📧  {ld['email']}    : {h['email']:<27}│\n"
        f"  └{'─'*46}┘\n"
    )


def S(title, icon, rows=None, note=None, links=None, card_helpline=None, warn=None, lang="en"):
    """
    Build a consistent structured response.
    """
    ld = LANG_DATA.get(lang, LANG_DATA["en"])
    out = [f"\n{DIV}", f"  {icon}  {title}", DIV]
    if warn:
        out.append(f"\n  ⚠️   {warn}")
    if rows:
        out.append("")
        for i, r in enumerate(rows, 1):
            out.append(f"  {i}.  {r}")
    if links:
        out.append("")
        for label, url in links:
            out.append(f"  🔗  {label}:")
            out.append(f"       {url}")
    if note:
        out.append(f"\n  💡  {ld['note']}: {note}")
    if card_helpline:
        out.append(helpline_box(card_helpline, lang))
    else:
        out.append(f"{DIV}\n")
    return "\n".join(out)


def out_of_scope(user_input, lang="en"):
    """Response for questions we cannot answer"""
    ld = LANG_DATA.get(lang, LANG_DATA["en"])
    q = user_input[:70] + ("..." if len(user_input) > 70 else "")
    
    # Satisfying translations for out of scope based on language
    if lang == "gu":
        title = "Aabhar!"
        msg = "Tamari vaat amari support team sudhi pahochi gai che. Te tamne khubaj jaldi sampark karse."
        direct = "Urgent madad mate niche na number par call karo:"
        topics = "Hu aa vishayo par madad kari saku chu:"
    elif lang == "pa":
        title = "Dhanwad!"
        msg = "Tuhadi query sadi support team nu mil gayi hai. Oh tuhade naal jaldi raabta karan ge."
        direct = "Urgent madad layi niche ditte number te call karo:"
        topics = "Main ena vishiyan te madad kar sakda han:"
    elif lang == "hi":
        title = "Dhanyawad!"
        msg = "Aapki query hamari support team tak pahonch gayi hai. Woh jald hi aap se sampark karenge."
        direct = "Urgent madad ke liye niche diye gaye number par call karein:"
        topics = "Main in topics par madad kar sakta hoon:"
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
        self.rag = RAGEngine()
        self.conversation_history = []
        
        self.intents = {
            "greet":             r"\b(hi+|hello|hey|namaste|namaskar|kem cho|satsriakal|adaab|helo|hey)\b",
            "goodbye":           r"\b(bye|goodbye|exit|quit|see you|alvida|tata|chalta hoon|avjo|rab rakha)\b",
            "app_not_working":   r"(app.*(not work|crash|error|open|load|issue|problem|start|nahi chal raha|kaam nahi kar|chalu nahi|nathi chaltu|nahi chalda))\b",
            "abha_download":     r"(download.*abha|abha.*download|abha card.*(get|le)|abha.*kaise.*(le|nikale|download)|abha.*kem.*download|abha.*kiven.*download)",
            "abha_create":       r"(abha.*(create|register|make|apply|new|bana)|create.*abha|abha.*kaise.*bana|abha.*kem.*banavu|abha.*kiven.*banaye)",
            "abha_info":         r"\b(abha|health id|health account|14.digit|ye kya hai|shu che|ki hai|vistar)\b",
            "ayushman_download": r"(ayushman.*(download|get|card|golden|le)|golden.*card|ayushman.*kaise.*(le|download)|ayushman.*kem.*download|ayushman.*kiven.*download)",
            "ayushman_info":     r"\b(ayushman|pmjay|jan arogya|5 lakh|health insurance|bima|scheme|yojana)\b",
            "covid_download":    r"(covid.*(certificate|cert|download|vaccination|le)|vaccine.*cert|covid.*kaise.*(le|download)|covid.*kem.*download|covid.*kiven.*download)",
            "covid_info":        r"\b(covid|corona|vaccination|vaccine|covishield|covaxin|teeka|tika)\b",
            "app_download":      r"(download.*app|app.*download|install.*aarogya|play store|app.*kahan.*milega|app.*kem.*download|app.*kiven.*download)",
            "app_upload":        r"(upload|add.*document|prescription.*upload|report.*upload|file.*kaise.*daalein|kahan.*upload)",
            "app_appointment":   r"(appointment|book|doctor.*milna|doctor.*dikhao|checkup|meeting|schedule)",
            "app_link_abha":     r"(link.*abha|abha.*connect|abha.*kaise.*jodein|abha.*kem.*link|abha.*kiven.*link)",
            "app_share":         r"(share.*record|send.*record|doctor.*bhejo|whatsapp.*bhejo|file.*share)",
            "app_view":          r"(view.*record|see.*record|my record|puraana report|report.*dikhao|pichela record)",
            "app_info":          r"\b(aarogyaone|aarogya one|phr app|health app|ye app.*kya|app.*shu che|app.*ki hai)\b",
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

    def get_rag_response(self, query, min_score=0.12):
        best, answers = self.rag.get_answer(query, top_k=2)
        if not answers or answers[0]["score"] < min_score:
            return None
        lines = [l.strip() for l in best.strip().split(". ") if l.strip()]
        return (
            f"\n{DIV}\n"
            f"  ℹ️   Information\n"
            f"{DIV}\n\n"
            + "\n".join(f"  •  {l}" for l in lines)
            + f"\n{DIV}\n"
        )

    def build_response(self, intents, user_input, lang="en"):
        responses = []
        ld = LANG_DATA.get(lang, LANG_DATA["en"])
        
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

        # Handle Greet
        if "greet" in intents:
            responses.append(
                f"\n{DIV}\n"
                f"  🙏  {ld['greet']}\n"
                f"{DIV}\n"
                f"\n  {ld['help_list']}\n"
                f"  📋  {ld['abha_name']:<18} — summarize / download\n"
                f"  🥇  {ld['ayushman_name']:<18} — eligibility / download\n"
                f"  💉  {ld['covid_name']:<18} — information / download\n"
                f"  📱  {ld['app_name']:<18} — features / guide\n"
                f"\n  {ld['ask_assist']}\n"
                f"{DIV}\n"
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
                if lang == "gu":
                    rows = ["ABHA ek 14-digit digital health ID che", "Badha health records ek j jagya e save karva mate", "Navu banavva: Type 'Create ABHA'", "Download karva: Type 'Download ABHA'"]
                elif lang == "hi":
                    rows = ["ABHA ek 14-digit digital health ID hai", "Saare medical records ek jagah manage karne ke liye", "Naya banane ke liye: Type 'Create ABHA'", "Download karne ke liye: Type 'Download ABHA'"]
                else:
                    rows = ["ABHA is a 14-digit unique health ID for all Indians", "Store and share medical records digitally", "To Create: Type 'Create ABHA'", "To Download: Type 'Download ABHA'"]
                responses.append(S(f"Summary: {ld['abha_name']}", "🏥", rows=rows, lang=lang, card_helpline="abha"))

            elif intent == "ayushman_info":
                if lang == "gu":
                    rows = ["Varshik 5 Lakh sudhi ni free sarvar", "Badhi moti bimari ane operation cover thay che", "Cashless treatment 25,000+ hospital ma avilable", "Download karva: Type 'Download Ayushman'"]
                elif lang == "hi":
                    rows = ["Sanaana 5 Lakh tak ka free mufat ilaaj", "Saari badi bimariyan aur operation cover hote hain", "25,000+ hospitals mein cashless suvidha", "Download karne ke liye: Type 'Download Ayushman'"]
                else:
                    rows = ["Rs 5 Lakh free health cover per family per year", "Covers major surgeries and hospital treatments", "Cashless at 25,000+ empanelled hospitals", "To Download: Type 'Download Ayushman'"]
                responses.append(S(f"Summary: {ld['ayushman_name']}", "🥇", rows=rows, lang=lang, card_helpline="ayushman"))

            elif intent == "covid_info":
                if lang == "gu":
                    rows = ["Tamara COVID vaccination nu digital proof", "Dose 1 ane Dose 2 ni mahiti hoy che", "Travel mate international level e manya che", "Download karva: Type 'Download Covid'"]
                elif lang == "hi":
                    rows = ["Aapke vaccination ka digital proof", "Dose 1 aur Dose 2 ki jaankari hoti hai", "Puri duniya mein travel ke liye manya hai", "Download karne ke liye: Type 'Download Covid'"]
                else:
                    rows = ["Digital proof of your COVID-19 vaccination", "Contains dose details and dates", "Internationally recognized for travel", "To Download: Type 'Download Covid'"]
                responses.append(S(f"Summary: {ld['covid_name']}", "💉", rows=rows, lang=lang, card_helpline="covid"))

            elif intent == "app_info":
                if lang == "gu":
                    rows = ["Tamara health records manage karvani free app", "Documents upload karo ane share karo", "Doctor ni appointment book karo", "ABHA ne connect karine records sync karo"]
                elif lang == "hi":
                    rows = ["Health records manage karne ki mufat app", "Documents upload aur share karein", "Doctor appointments book karein", "ABHA connect karke records sync karein"]
                else:
                    rows = ["Free app to manage your personal health records", "Upload and share documents securely", "Book doctor appointments from phone", "Link ABHA to sync your medical history"]
                responses.append(S(f"Summary: {ld['app_name']}", "📱", rows=rows, lang=lang, card_helpline="aarogyaone"))

            elif intent == "app_appointment":
                if lang == "gu":
                    rows = ["AarogyaOne PHR app kholo", "Home screen par 'Book Appointment' par click karo", "Doctor nu naam ke specialty thi search karo", "Tarikh ane samay slot pasand karo", "Appointment confirm karo"]
                elif lang == "hi":
                    rows = ["AarogyaOne PHR app kholein", "Home screen par 'Book Appointment' par click karein", "Doctor ka naam ya specialty se search karein", "Date aur time slot chunein", "Appointment confirm karein"]
                elif lang == "pa":
                    rows = ["AarogyaOne PHR app kholo", "Home screen te 'Book Appointment' te click karo", "Doctor de naam ya specialty naal search karo", "Date te time slot chuno", "Appointment confirm karo"]
                else:
                    rows = ["Open AarogyaOne PHR App", "Click 'Book Appointment' on Home Screen", "Search Doctor by name or specialty", "Select Date and Time Slot", "Confirm your Appointment"]
                responses.append(S(f"{ld['app_name']} Appointment", "📅", rows=rows, lang=lang, card_helpline="aarogyaone"))

            elif intent == "abha_download":
                if lang == "gu":
                    rows = ["abdm.gov.in par jao", "Login par click karo", "Mobile number nakho", "OTP thi verify karo", "ABHA card download karo"]
                elif lang == "hi":
                    rows = ["abdm.gov.in par jayein", "Login par click karein", "Mobile number dalein", "OTP se verify karein", "ABHA card download karein"]
                else:
                    rows = ["Visit abdm.gov.in", "Click 'Download ABHA Card'", "Enter mobile number", "Verify with OTP", "Card downloads as PDF"]
                responses.append(S(f"{ld['abha_name']} Download", "📥", rows=rows, lang=lang, card_helpline="abha"))

            elif intent == "abha_create":
                if lang == "gu":
                    rows = ["abdm.gov.in par jao", "Create ABHA par click karo", "Aadhaar number nakho", "OTP thi verify karo", "Detail bhari ne card download karo"]
                elif lang == "hi":
                    rows = ["abdm.gov.in par jayein", "Create ABHA par click karein", "Aadhaar number dalein", "OTP se verify karein", "Detail bhar ke card download karein"]
                else:
                    rows = ["Visit abdm.gov.in", "Click 'Create ABHA'", "Enter Aadhaar number", "Verify with OTP", "Fill details and download PDF"]
                responses.append(S(f"{ld['abha_name']} Create", "📝", rows=rows, lang=lang, card_helpline="abha"))

            elif intent == "covid_download":
                if lang == "gu":
                    rows = ["www.cowin.gov.in par jao", "Register par click karo", "Mobile number nakho", "OTP thi login karo", "Certificate download karo"]
                elif lang == "hi":
                    rows = ["www.cowin.gov.in par jayein", "Register par click karein", "Mobile number dalein", "OTP se login karein", "Certificate download karein"]
                else:
                    rows = ["Visit www.cowin.gov.in", "Click 'Register/Sign In'", "Enter mobile number", "Verify with OTP", "Download Certificate"]
                responses.append(S(f"{ld['covid_name']} Download", "💉", rows=rows, lang=lang, card_helpline="covid"))

            elif intent == "app_not_working":
                responses.append(
                    f"\n{DIV}\n"
                    f"  ⚠️   {ld['app_name']} Issue?\n"
                    f"{DIV}\n"
                    f"\n  {ld['fix_steps']}\n"
                    f"  1.  Force close and reopen the app\n"
                    f"  2.  Check your internet connection\n"
                    f"  3.  Update app from Google Play Store\n"
                    f"  4.  Clear app cache in phone settings\n"
                    f"  5.  Reinstall if problem continues\n"
                    f"\n  {ld['still_not_working']}"
                    f"{helpline_box('aarogyaone', lang)}"
                )

            elif intent == "helpline":
                responses.append(
                    f"\n{DIV}\n"
                    f"  📞  India Health Helplines\n"
                    f"{DIV}\n"
                    f"\n  🚑  Ambulance          :  108\n"
                    f"  🏥  Health Helpline    :  104\n"
                    f"  💉  CoWIN / COVID      :  1075\n"
                    f"  🥇  Ayushman Bharat    :  14555\n"
                    f"  📋  ABHA / ABDM        :  1800-11-4477\n"
                    f"{DIV}\n"
                )

        if not responses and "unknown" in intents:
            rag = self.get_rag_response(user_input)
            if rag:
                return rag
            return out_of_scope(user_input, lang)

        return "\n".join(responses)

    def chat(self, user_input):
        user_input = user_input.strip()
        if not user_input:
            return f"\n{DIV}\n  🤔  Type a message.\n{DIV}\n"

        lang = self.detect_language(user_input)
        self.conversation_history.append({"role": "user", "text": user_input, "lang": lang})
        
        intents = self.detect_intent(user_input)
        response = self.build_response(intents, user_input, lang)
        
        self.conversation_history.append({"role": "bot", "text": response})
        return response


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