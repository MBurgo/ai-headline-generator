import streamlit as st
from headline_engine import generate_headline_variants

# --- Page setup
st.set_page_config(
    page_title="Burgo's Copywriting Framework Headline Rewriter",
    layout="centered",
    initial_sidebar_state="auto",
    page_icon="🧠"
)

# --- Custom styles (using Roboto + brand colors)
st.write('''
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Roboto:wght@400;500;700&display=swap');

        html, body, [class*="css"] {
            font-family: 'Roboto', sans-serif !important;
        }

        .main {
            background-color: #fdf5da !important;
            padding: 2rem;
        }

        .headline-box {
            background-color: #fff6e0;
            border-left: 6px solid #ffb81c;
            padding: 1rem;
            margin-top: 1rem;
            border-radius: 6px;
            color: #1c1d20 !important;
            font-size: 1.1rem;
            line-height: 1.4;
        }

        .score-label {
            font-weight: 500;
            font-size: 0.9rem;
            color: #53565a;
        }

        .score-box {
            background-color: #e7ebf8;
            padding: 0.75rem 1rem;
            border-radius: 6px;
            font-size: 0.9rem;
            font-weight: 500;
            color: #1c1d20;
            margin-top: 0.5rem;
        }

        .stExpander > div > div {
            padding: 1rem;
        }

        h1 {
            font-size: 2rem;
            color: #1c1d20;
        }

        .stTextInput label, .stSelectbox label, .stTextArea label {
            font-weight: 600;
            font-size: 1rem;
        }

        .stButton button {
            background-color: #ffb81c !important;
            color: #1c1d20 !important;
            border: none;
            padding: 0.5rem 1rem;
            border-radius: 6px;
            font-weight: bold;
        }
    </style>
''', unsafe_allow_html=True)

# --- Title
st.title("🧠 Burgo's Copywriting Framework Headline Rewriter")
st.markdown("Enter a headline and our AI will rewrite it using proven copywriting frameworks — like AIDA, PAS, BAB, and more — complete with emotional analysis.")

# --- Input fields (reordered)
use_case = st.selectbox(
    "📌 What is this headline for?",
    [
        "Facebook ad",
        "Sales email subject line",
        "Landing page hero headline",
        "Sales order page headline",
        "YouTube ad overlay headline"
    ],
    index=0
)

input_headline = st.text_input("✍️ Your headline", placeholder="e.g. This ASX stock could skyrocket by next earnings season")

audience_insight = None
with st.expander("🎯 Advanced (optional): Tell us more about your audience"):
    audience_insight = st.text_input(
        "Who is this for?",
        placeholder="e.g. Retirees, under 35s, first-time investors, income-focused investors, etc."
    )

# --- Generate button
if st.button("Generate Headline Variations"):
    if not input_headline:
        st.warning("Please enter a headline first.")
    else:
        with st.spinner("Generating headline rewrites..."):
            results = generate_headline_variants(input_headline, use_case, audience_insight)

        st.success("Done! Scroll down to see the results.")

        for result in results:
            with st.expander(f"📚 {result['framework']}", expanded=False):
                st.markdown(f"""
                <div class="headline-box">
                    <strong>Headline:</strong><br>
                    {result['headline']}
                </div>
                """, unsafe_allow_html=True)

                st.markdown(f"<span class='score-label'>{result['explanation']}</span>", unsafe_allow_html=True)

                scores = result.get("emotional_leverage", {})
                if scores:
                    st.markdown("<br><span class='score-label'>🧠 Emotional Leverage Score:</span>", unsafe_allow_html=True)

                    score_display = f"""
                    <div class="score-box">
                        🎯 <strong>Trigger:</strong> {scores.get('Primary emotional trigger', '—')}<br>
                        🧲 <strong>Curiosity:</strong> {scores.get('Curiosity', '—')}<br>
                        🧼 <strong>Clarity:</strong> {scores.get('Clarity', '—')}<br>
                        📌 <strong>Specificity:</strong> {scores.get('Specificity', '—')}<br>
                        ⏳ <strong>Urgency:</strong> {scores.get('Urgency', '—')}
                    </div>
                    """
                    st.markdown(score_display, unsafe_allow_html=True)

        st.markdown("---")
        st.caption("Powered by OpenAI · Built by you 🚀")
