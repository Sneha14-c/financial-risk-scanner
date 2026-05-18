# =========================
# IMPORTS
# =========================
import re
import streamlit as st
import ollama
from pypdf import PdfReader

# =========================
# CONFIG
# =========================
CHAT_MODEL = "gemma:2b"
MAX_CONTEXT_CHARS = 3000

st.set_page_config(page_title="Financial Risk Scanner", layout="wide")

# =========================
# LANGUAGE SELECT
# =========================
language = st.sidebar.selectbox(
    "Language / भाषा / ಭಾಷೆ",
    ["English", "Hindi", "Kannada"]
)

# =========================
# TEXT MAP
# =========================
TEXT = {
    "English": {
        "title": "📄 Financial Document Risk Scanner",
        "profile": "Investor Profile",
        "age": "Investor Age",
        "income": "Annual Income (₹)",
        "upload": "Upload Policy Document (PDF or TXT)",
        "process": "🔍 Process Document",
        "summary": "📑 Generate Risk Summary",
        "clauses": "Extracted Risk Clauses",
        "overview": "Risk Assessment Overview",
        "level": "Risk Level",
        "score": "Risk Score",
        "structured": "Structured Risk Summary",
        "caption": "AI-assisted financial risk assessment. Not legal advice.",
        "processing": "Processing document...",
        "generating": "Generating summary..."
    },
    "Hindi": {
        "title": "📄 वित्तीय दस्तावेज़ जोखिम विश्लेषक",
        "profile": "निवेशक प्रोफ़ाइल",
        "age": "निवेशक आयु",
        "income": "वार्षिक आय (₹)",
        "upload": "पॉलिसी दस्तावेज़ अपलोड करें",
        "process": "🔍 दस्तावेज़ विश्लेषण करें",
        "summary": "📑 जोखिम सारांश तैयार करें",
        "clauses": "निकाले गए जोखिम प्रावधान",
        "overview": "जोखिम मूल्यांकन अवलोकन",
        "level": "जोखिम स्तर",
        "score": "जोखिम स्कोर",
        "structured": "संरचित जोखिम सारांश",
        "caption": "एआई आधारित जोखिम विश्लेषण। यह कानूनी सलाह नहीं है।",
        "processing": "दस्तावेज़ संसाधित किया जा रहा है...",
        "generating": "सारांश तैयार किया जा रहा है..."
    },
    "Kannada": {
        "title": "📄 ಹಣಕಾಸು ದಾಖಲೆ ಅಪಾಯ ವಿಶ್ಲೇಷಕ",
        "profile": "ಹೂಡಿಕೆದಾರರ ಪ್ರೊಫೈಲ್",
        "age": "ಹೂಡಿಕೆದಾರರ ವಯಸ್ಸು",
        "income": "ವಾರ್ಷಿಕ ಆದಾಯ (₹)",
        "upload": "ಪಾಲಿಸಿ ದಾಖಲೆ ಅಪ್‌ಲೋಡ್ ಮಾಡಿ",
        "process": "🔍 ದಾಖಲೆ ವಿಶ್ಲೇಷಿಸಿ",
        "summary": "📑 ಅಪಾಯ ಸಾರಾಂಶ ರಚಿಸಿ",
        "clauses": "ಪತ್ತೆಯಾದ ಅಪಾಯ ವಿಧಿಗಳು",
        "overview": "ಅಪಾಯ ಮೌಲ್ಯಮಾಪನ ಅವಲೋಕನ",
        "level": "ಅಪಾಯ ಮಟ್ಟ",
        "score": "ಅಪಾಯ ಅಂಕ",
        "structured": "ರಚಿತ ಅಪಾಯ ಸಾರಾಂಶ",
        "caption": "ಎಐ ಆಧಾರಿತ ಅಪಾಯ ವಿಶ್ಲೇಷಣೆ. ಇದು ಕಾನೂನು ಸಲಹೆ ಅಲ್ಲ.",
        "processing": "ದಾಖಲೆ ಪ್ರಕ್ರಿಯೆಗೊಳಿಸಲಾಗುತ್ತಿದೆ...",
        "generating": "ಸಾರಾಂಶ ರಚಿಸಲಾಗುತ್ತಿದೆ..."
    }
}

T = TEXT[language]

# =========================
# TITLE
# =========================
st.title(T["title"])

# =========================
# INVESTOR PROFILE
# =========================
st.sidebar.header(T["profile"])
age = st.sidebar.number_input(T["age"], 18, 80, 30)
annual_income = st.sidebar.number_input(T["income"], 100000, 2000000, 500000)

# =========================
# FILE EXTRACTION
# =========================
def extract_text_from_file(uploaded_file):
    if uploaded_file.type == "text/plain":
        return uploaded_file.read().decode("utf-8")
    elif uploaded_file.type == "application/pdf":
        reader = PdfReader(uploaded_file)
        text = ""
        for page in reader.pages:
            content = page.extract_text()
            if content:
                text += content + "\n"
        return text
    return ""

# =========================
# DOCUMENT RISK LOGIC
# =========================
def process_document(text):

    keywords = [
        "year", "%", "return",
        "commission", "charge",
        "penalty", "increase",
        "reserves the right"
    ]

    lines = text.split("\n")
    relevant = []

    for line in lines:
        for word in keywords:
            if word in line.lower():
                relevant.append(line)
                break

    extracted_text = "\n".join(relevant)[:MAX_CONTEXT_CHARS]

    risk_score = 0
    text_lower = text.lower()

    if re.search(r'(\d+)\s*year', text_lower):
        risk_score += 20

    percentages = re.findall(r'(\d+)%', text_lower)
    for p in percentages:
        if int(p) > 50:
            risk_score += 20
            break

    if re.search(r'increase.*?(\d+)%', text_lower):
        risk_score += 20

    if "reserves the right" in text_lower:
        risk_score += 10

    return extracted_text, risk_score

# =========================
# AGE & INCOME ADJUSTMENT
# =========================
def adjust_risk(score):

    age_adj = 5 if age < 25 else 5 if 41 <= age <= 55 else 10 if age > 55 else 0
    income_adj = 10 if annual_income < 300000 else 5 if annual_income < 800000 else 0

    final_score = min(score + age_adj + income_adj, 100)

    if final_score >= 60:
        base = "High"
    elif final_score >= 30:
        base = "Medium"
    else:
        base = "Low"

    if language == "Hindi":
        map_level = {"High": "उच्च", "Medium": "मध्यम", "Low": "कम"}
    elif language == "Kannada":
        map_level = {"High": "ಉನ್ನತ", "Medium": "ಮಧ್ಯಮ", "Low": "ಕಡಿಮೆ"}
    else:
        map_level = {"High": "High", "Medium": "Medium", "Low": "Low"}

    return final_score, map_level[base], base

# =========================
# SUMMARY GENERATION
# =========================
# =========================
# SUMMARY GENERATION
# =========================
def generate_summary(extracted, score, level):

    # Language-specific headings
    if language == "Hindi":
        h1 = "## समग्र वित्तीय जोखिम"
        h2 = "## कानूनी जोखिम"
        h3 = "## दीर्घकालिक प्रभाव"
        h4 = "## जोखिम वर्गीकरण"
        h5 = "## निवेशक सिफारिशें"
        lang_instruction = "पूरा उत्तर केवल हिंदी में लिखें। किसी भी प्रकार का अंग्रेज़ी शब्द उपयोग न करें।"
        age_income_line = f"निवेशक की आयु {age} वर्ष है और वार्षिक आय ₹{annual_income} है। विश्लेषण में इन दोनों का प्रभाव स्पष्ट रूप से शामिल करें।"

    elif language == "Kannada":
        h1 = "## ಒಟ್ಟು ಹಣಕಾಸು ಅಪಾಯ"
        h2 = "## ಕಾನೂನು ಅಪಾಯ"
        h3 = "## ದೀರ್ಘಕಾಲಿಕ ಪರಿಣಾಮ"
        h4 = "## ಅಪಾಯ ವರ್ಗೀಕರಣ"
        h5 = "## ಹೂಡಿಕೆದಾರರ ಶಿಫಾರಸುಗಳು"
        lang_instruction = "ಸಂಪೂರ್ಣ ಉತ್ತರವನ್ನು ಕನ್ನಡದಲ್ಲಿ ಮಾತ್ರ ಬರೆಯಿರಿ. ಯಾವುದೇ ಇಂಗ್ಲಿಷ್ ಪದಗಳನ್ನು ಬಳಸಬೇಡಿ."
        age_income_line = f"ಹೂಡಿಕೆದಾರರ ವಯಸ್ಸು {age} ವರ್ಷ ಮತ್ತು ವಾರ್ಷಿಕ ಆದಾಯ ₹{annual_income} ಆಗಿದೆ. ಈ ಎರಡು ಅಂಶಗಳ ಪರಿಣಾಮವನ್ನು ವಿಶ್ಲೇಷಣೆಯಲ್ಲಿ ಸ್ಪಷ್ಟವಾಗಿ ಸೇರಿಸಿ."

    else:
        h1 = "## Overall Financial Exposure"
        h2 = "## Legal Vulnerability"
        h3 = "## Long-Term Risk Impact"
        h4 = "## Risk Severity Classification"
        h5 = "## Advisory Recommendation"
        lang_instruction = "Write the entire response strictly in English."
        age_income_line = f"The investor is {age} years old with an annual income of ₹{annual_income}. Clearly integrate how age and income influence risk exposure."

    # Step 1: Generate structured summary
    base_prompt = f"""
You MUST follow the structure EXACTLY.
Do NOT change headings.
Do NOT add extra sections.

{lang_instruction}

Output EXACTLY in this format:

{h1}
(5-7 sentences including age and income impact)

{h2}
(5-7 sentences)

{h3}
(5-7 sentences)

{h4}
(Explain clearly why overall risk is {level})

{h5}
(Provide practical investor actions)

---------------------------------

Risk Score: {score}
Risk Level: {level}
{age_income_line}

Extracted Clauses:
{extracted}
"""

    response = ollama.chat(
        model=CHAT_MODEL,
        messages=[{"role": "user", "content": base_prompt}],
        options={
            "num_predict": 1000,
            "temperature": 0.05
        }
    )

    summary_text = response["message"]["content"]

    # Step 2: Enforce language strictly (second pass cleanup)
    if language != "English":
        enforce_prompt = f"""
Rewrite the following text fully in {language}.
Remove any English words completely.
Keep meaning same.
Do NOT change headings.

Text:
{summary_text}
"""
        response2 = ollama.chat(
            model=CHAT_MODEL,
            messages=[{"role": "user", "content": enforce_prompt}],
            options={
                "num_predict": 1000,
                "temperature": 0.0
            }
        )
        return response2["message"]["content"]

    return summary_text
# =========================
# FILE UPLOAD
# =========================
uploaded_file = st.file_uploader(T["upload"], type=["pdf", "txt"])

if uploaded_file:

    document_text = extract_text_from_file(uploaded_file)

    col1, col2 = st.columns(2)

    if col1.button(T["process"]):
        with st.spinner(T["processing"]):
            extracted, base_score = process_document(document_text)
            final_score, level_translated, base_level = adjust_risk(base_score)

            st.session_state.extracted = extracted
            st.session_state.score = final_score
            st.session_state.level = level_translated
            st.session_state.base_level = base_level

    if col2.button(T["summary"]):
        if "extracted" in st.session_state:
            with st.spinner(T["generating"]):
                st.session_state.summary = generate_summary(
                    st.session_state.extracted,
                    st.session_state.score,
                    st.session_state.level
                )

    st.markdown("---")

    # SHOW CLAUSES (Original – No Translation)
    if "extracted" in st.session_state:
        st.subheader(T["clauses"])
        st.text_area("", st.session_state.extracted, height=200)

    # SHOW RISK
    if "score" in st.session_state:
        st.subheader(T["overview"])

        if st.session_state.base_level == "High":
            st.error(f"{T['level']}: {st.session_state.level}")
        elif st.session_state.base_level == "Medium":
            st.warning(f"{T['level']}: {st.session_state.level}")
        else:
            st.success(f"{T['level']}: {st.session_state.level}")

        st.progress(st.session_state.score / 100)
        st.markdown(f"**{T['score']}:** {st.session_state.score}/100")

    # SHOW SUMMARY
    if "summary" in st.session_state:
        st.subheader(T["structured"])
        st.markdown(st.session_state.summary)

    st.caption(T["caption"])