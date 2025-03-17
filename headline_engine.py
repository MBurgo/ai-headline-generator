import streamlit as st
import openai

# Use Streamlit secrets for OpenAI key
client = openai.OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

def call_openai(prompt, model="gpt-4o", temperature=0.7):
    response = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}],
        temperature=temperature
    )
    return response.choices[0].message.content.strip()

def explain_framework(name):
    explanations = {
        "AIDA": "Attention, Interest, Desire, Action – a classic flow from hook to call-to-action.",
        "PAS": "Problem, Agitate, Solution – highlight the pain, make it sting, then offer relief.",
        "BAB": "Before, After, Bridge – show the current pain, ideal future, and how to get there.",
        "FAB": "Features, Advantages, Benefits – move from what it is to why it matters.",
        "4 U’s": "Urgent, Unique, Useful, Ultra-specific – especially for headlines and hooks.",
        "5 P’s": "Promise, Picture, Prove, Push, Personal – strong offer-driven persuasion.",
        "Persuasion Equation": "Urgent Problem, Unique Promise, Unquestionable Proof, User-friendly Proposition."
    }
    return explanations.get(name, "")

def get_use_case_prompt(use_case):
    prompts = {
        "Facebook ad": "Write a short, emotionally engaging headline for a Facebook ad. It should grab attention quickly in a crowded feed. Focus on curiosity, urgency, or a bold benefit. Keep it short and scroll-stopping. Avoid overly formal tone.",
        "Sales email subject line": "Write a subject line for a marketing email. It must be concise (under ~50 characters is ideal), spark curiosity or highlight a specific benefit, and feel personal or timely. Avoid excessive punctuation, all-caps, or hype.",
        "Landing page hero headline": "Write a headline for the top of a landing page. It should clearly communicate the main benefit or value proposition. Prioritise clarity and motivation — give people a reason to keep reading or scrolling.",
        "Sales order page headline": "Write a headline for the top of a sales order page. Its job is to reassure the user that they’re making a smart decision. Focus on trust, proof, satisfaction, or reminder of value. Avoid new or untested claims.",
        "YouTube ad overlay headline": "Write a text overlay or lead-in headline for a YouTube ad. It should be visually compelling and grab attention quickly. Use intrigue or a bold benefit — keep it short and readable in 1–2 seconds. Avoid long sentences or subtlety."
    }
    return prompts.get(use_case, "")

def score_emotions(headline):
    scoring_prompt = f"""
Analyze this headline and score it (0 to 1) on:
- Primary emotional trigger (choose one): Fear, Curiosity, Hope, Authority, Greed, Belonging, Logic
- Curiosity
- Clarity
- Specificity
- Urgency

Return as JSON.

Headline: "{headline}"
"""
    try:
        response = call_openai(scoring_prompt, model="gpt-4", temperature=0)
        return eval(response)
    except Exception as e:
        print("Error in scoring:", e)
        return {}

def generate_headline_variants(input_headline, use_case, audience_insight=None):
    use_case_instruction = get_use_case_prompt(use_case)
    audience_line = f"\nAudience insight: {audience_insight.strip()}" if audience_insight else ""

    context_intro = f"""You are writing a single, natural-sounding headline for an ad promoting a free stock report.

Audience: Beginner ASX investors  
Offer: A free report with expert stock recommendations  
Benefit: Spotting breakout ASX stocks before they go mainstream  
Use case: {use_case}  
Instruction: {use_case_instruction}{audience_line}

Avoid generic language like “boost your portfolio” or “unlock hidden potential.” Avoid repeating phrasing from other frameworks. Use bold, conversational, human copy that sounds like a real ad or email subject line. Prioritise curiosity, clarity, urgency, and specificity. Keep it compliant — don’t overpromise or use exaggerated claims."""

    frameworks = {
        "AIDA": f"""{context_intro}

Framework: AIDA – Attention, Interest, Desire, Action  
Example: "This Overlooked ASX Stock Just Got a $1 Billion Boost — See Why Investors Are Rushing In Today"

Now rewrite this headline using the AIDA framework:

Original headline: {input_headline}
Rewritten headline:""",

        "PAS": f"""{context_intro}

Framework: PAS – Problem, Agitate, Solution  
Example: "Missing Out on ASX Gains? Here’s the Stock That Could Turn It Around Fast"

Now rewrite this headline using the PAS framework:

Original headline: {input_headline}
Rewritten headline:""",

        "BAB": f"""{context_intro}

Framework: BAB – Before, After, Bridge  
Example: "Stuck in underperforming ETFs? Get targeted growth with expert-backed ASX picks. Start your shift today."

Now rewrite this headline using the BAB framework:

Original headline: {input_headline}
Rewritten headline:""",

        "FAB": f"""{context_intro}

Framework: FAB – Features, Advantages, Benefits  
Example: "2 Expert Picks Per Month With Insights From ASX Analysts So You Can Build Wealth Smarter"

Now rewrite this headline using the FAB framework:

Original headline: {input_headline}
Rewritten headline:""",

        "4 U’s": f"""{context_intro}

Framework: 4 U’s – Urgent, Unique, Useful, Ultra-specific  
Example: "Last Chance: Our #1 ASX Pick for March — Backed by 237% Historical Returns"

Now rewrite this headline using the 4 U’s framework:

Original headline: {input_headline}
Rewritten headline:""",

        "5 P’s": f"""{context_intro}

Framework: 5 P’s – Promise, Picture, Prove, Push, Personal  
Example: "This One Stock Could Accelerate Your Portfolio — See the Track Record and Why 100,000 Aussies Already Trust Us"

Now rewrite this headline using the 5 P’s framework:

Original headline: {input_headline}
Rewritten headline:""",

        "Persuasion Equation": f"""{context_intro}

Framework: Persuasion Equation – Urgent Problem, Unique Promise, Unquestionable Proof, User-friendly Proposition  
Example: "Struggling to Find Reliable ASX Stocks? Our Free Report Reveals a Unique, Proven Winner — Download It Instantly"

Now rewrite this headline using the Persuasion Equation:

Original headline: {input_headline}
Rewritten headline:"""
    }

    output = []
    for name, framework_prompt in frameworks.items():
        try:
            new_headline = call_openai(framework_prompt)
            emotional_scores = score_emotions(new_headline)
        except Exception as e:
            new_headline = "Error generating headline."
            emotional_scores = {}

        output.append({
            "framework": name,
            "headline": new_headline,
            "explanation": explain_framework(name),
            "emotional_leverage": emotional_scores
        })

    return output
