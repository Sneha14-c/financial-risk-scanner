# =========================
# IMPORTS
# =========================
import re
import streamlit as st
from pypdf import PdfReader

# =========================
# CONFIG
# =========================
MAX_CONTEXT_CHARS = 3000

st.set_page_config(
    page_title=" Financial Risk Scanner",
    layout="wide"
)

# =========================
# LANGUAGE SELECT
# =========================
language = st.sidebar.selectbox(
    "Language / भाषा / ಕನ್ನಡ",
    ["English", "Hindi", "Kannada"]
)

# =========================
# TEXT MAP
# =========================
TEXT = {

    "English": {
        "title": "📄  Financial Risk Scanner",
        "profile": "Investor Profile",
        "age": "Investor Age",
        "income": "Annual Income (₹)",
        "upload": "Upload Financial Document (PDF or TXT)",
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
        "upload": "वित्तीय दस्तावेज़ अपलोड करें",
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
        "upload": "ಹಣಕಾಸು ದಾಖಲೆ ಅಪ್‌ಲೋಡ್ ಮಾಡಿ",
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

age = st.sidebar.number_input(
    T["age"],
    18,
    80,
    30
)

annual_income = st.sidebar.number_input(
    T["income"],
    100000,
    2000000,
    500000
)

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
# DOCUMENT PROCESSING
# =========================
def process_document(text):

    keywords = [
        "year",
        "%",
        "return",
        "commission",
        "charge",
        "penalty",
        "increase",
        "loan",
        "debt",
        "loss",
        "liability",
        "interest",
        "default",
        "reserves the right"
    ]

    lines = text.split("\n")

    relevant = []

    for line in lines:

        for word in keywords:

            if word.lower() in line.lower():
                relevant.append(line)
                break

    extracted_text = "\n".join(relevant)[:MAX_CONTEXT_CHARS]

    # =========================
    # RISK SCORE LOGIC
    # =========================
    risk_score = 0

    text_lower = text.lower()

    # Long-term commitment
    if re.search(r'(\d+)\s*year', text_lower):
        risk_score += 15

    # High percentages
    percentages = re.findall(r'(\d+)%', text_lower)

    for p in percentages:

        if int(p) > 50:
            risk_score += 20
            break

    # Financial keywords
    if "loan" in text_lower:
        risk_score += 15

    if "debt" in text_lower:
        risk_score += 15

    if "loss" in text_lower:
        risk_score += 15

    if "liability" in text_lower:
        risk_score += 10

    if "default" in text_lower:
        risk_score += 10

    if "interest" in text_lower:
        risk_score += 5

    if "reserves the right" in text_lower:
        risk_score += 10

    return extracted_text, risk_score

# =========================
# RISK ADJUSTMENT
# =========================
def adjust_risk(score):

    # Age adjustment
    if age < 25:
        age_adj = 5

    elif age > 55:
        age_adj = 10

    else:
        age_adj = 0

    # Income adjustment
    if annual_income < 300000:
        income_adj = 10

    elif annual_income < 800000:
        income_adj = 5

    else:
        income_adj = 0

    final_score = min(score + age_adj + income_adj, 100)

    if final_score >= 60:
        base_level = "High"

    elif final_score >= 30:
        base_level = "Medium"

    else:
        base_level = "Low"

    # Translation
    if language == "Hindi":

        mapping = {
            "High": "उच्च",
            "Medium": "मध्यम",
            "Low": "कम"
        }

    elif language == "Kannada":

        mapping = {
            "High": "ಉನ್ನತ",
            "Medium": "ಮಧ್ಯಮ",
            "Low": "ಕಡಿಮೆ"
        }

    else:

        mapping = {
            "High": "High",
            "Medium": "Medium",
            "Low": "Low"
        }

    return final_score, mapping[base_level], base_level

# =========================
# SUMMARY GENERATION
# =========================
def generate_summary(extracted, score, level):

    if language == "Hindi":

        summary = f"""
## वित्तीय जोखिम विश्लेषण

### समग्र जोखिम
दस्तावेज़ में कई वित्तीय जोखिम संकेत मिले हैं।
निवेशक की आय और आयु के आधार पर जोखिम मध्यम से उच्च है।

### जोखिम स्तर
जोखिम स्कोर: {score}/100
जोखिम स्तर: {level}

### प्रमुख जोखिम
- ऋण और देनदारियाँ मौजूद हैं
- वित्तीय हानि का संकेत मिला
- दीर्घकालिक भुगतान जोखिम
- उच्च वित्तीय बोझ

### सिफारिश
निवेश से पहले दस्तावेज़ की पूरी समीक्षा करें।
ऋण कम करें और सुरक्षित निवेश विकल्प चुनें।

### निकाले गए प्रावधान
{extracted}
"""

    elif language == "Kannada":

        summary = f"""
## ಹಣಕಾಸು ಅಪಾಯ ವಿಶ್ಲೇಷಣೆ

### ಒಟ್ಟು ಅಪಾಯ
ದಾಖಲೆಯಲ್ಲಿ ಹಲವು ಹಣಕಾಸು ಅಪಾಯ ಸೂಚನೆಗಳು ಕಂಡುಬಂದಿವೆ.
ಹೂಡಿಕೆದಾರರ ಆದಾಯ ಮತ್ತು ವಯಸ್ಸಿನ ಆಧಾರದ ಮೇಲೆ ಅಪಾಯ ಮಧ್ಯಮದಿಂದ ಉನ್ನತ ಮಟ್ಟದಲ್ಲಿದೆ.

### ಅಪಾಯ ಮಟ್ಟ
ಅಪಾಯ ಅಂಕ: {score}/100
ಅಪಾಯ ಮಟ್ಟ: {level}

### ಪ್ರಮುಖ ಅಪಾಯಗಳು
- ಸಾಲ ಮತ್ತು ಬಾಧ്യതೆಗಳು ಕಂಡುಬಂದಿವೆ
- ಹಣಕಾಸು ನಷ್ಟದ ಸೂಚನೆ
- ದೀರ್ಘಕಾಲಿಕ ಪಾವತಿ ಅಪಾಯ
- ಹೆಚ್ಚಿನ ಹಣಕಾಸು ಒತ್ತಡ

### ಶಿಫಾರಸು
ಹೂಡಿಕೆಗೆ ಮೊದಲು ದಾಖಲೆ ಸಂಪೂರ್ಣ ಪರಿಶೀಲಿಸಿ.
ಸಾಲವನ್ನು ಕಡಿಮೆ ಮಾಡಿ ಮತ್ತು ಸುರಕ್ಷಿತ ಹೂಡಿಕೆ ಆಯ್ಕೆಮಾಡಿ.

### ಪತ್ತೆಯಾದ ವಿಧಿಗಳು
{extracted}
"""

    else:

        summary = f"""
## Financial Risk Analysis

### Overall Financial Exposure
The uploaded document contains multiple financial risk indicators.
The investor profile and extracted clauses indicate moderate to high exposure.

### Risk Severity
Risk Score: {score}/100
Risk Level: {level}

### Key Risk Factors
- Debt and liabilities detected
- Financial losses identified
- Long-term repayment risks observed
- High operational financial burden

### Recommendation
It is recommended to reduce liabilities,
improve cash flow management,
and avoid high-risk investments.

### Extracted Clauses
{extracted}
"""

    return summary

# =========================
# FILE UPLOAD
# =========================
uploaded_file = st.file_uploader(
    T["upload"],
    type=["pdf", "txt"]
)

# =========================
# MAIN LOGIC
# =========================
if uploaded_file:

    document_text = extract_text_from_file(uploaded_file)

    col1, col2 = st.columns(2)

    # PROCESS BUTTON
    if col1.button(T["process"]):

        with st.spinner(T["processing"]):

            extracted, base_score = process_document(document_text)

            final_score, level_translated, base_level = adjust_risk(base_score)

            st.session_state.extracted = extracted
            st.session_state.score = final_score
            st.session_state.level = level_translated
            st.session_state.base_level = base_level

    # SUMMARY BUTTON
    if col2.button(T["summary"]):

        if "extracted" in st.session_state:

            with st.spinner(T["generating"]):

                st.session_state.summary = generate_summary(
                    st.session_state.extracted,
                    st.session_state.score,
                    st.session_state.level
                )

    st.markdown("---")

    # SHOW EXTRACTED CLAUSES
    if "extracted" in st.session_state:

        st.subheader(T["clauses"])

        st.text_area(
            "",
            st.session_state.extracted,
            height=200
        )

    # SHOW RISK OVERVIEW
    if "score" in st.session_state:

        st.subheader(T["overview"])

        if st.session_state.base_level == "High":

            st.error(
                f"{T['level']}: {st.session_state.level}"
            )

        elif st.session_state.base_level == "Medium":

            st.warning(
                f"{T['level']}: {st.session_state.level}"
            )

        else:

            st.success(
                f"{T['level']}: {st.session_state.level}"
            )

        st.progress(st.session_state.score / 100)

        st.markdown(
            f"**{T['score']}:** {st.session_state.score}/100"
        )

    # SHOW SUMMARY
    if "summary" in st.session_state:

        st.subheader(T["structured"])

        st.markdown(st.session_state.summary)

    st.caption(T["caption"])