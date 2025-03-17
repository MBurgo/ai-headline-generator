import streamlit as st
import openai

# Use Streamlit secrets for OpenAI key
client = openai.OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

def call_openai(system_prompt, user_prompt, model="gpt-4o", temperature=0.7):
    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
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

Headline: \"{headline}\"
"""
    try:
        response = call_openai("You are a helpful assistant.", scoring_prompt, model="gpt-4", temperature=0)
        return eval(response)
    except Exception as e:
        print("Error in scoring:", e)
        return {}

def generate_headline_variants(input_headline, use_case, audience_insight=None):
    use_case_instruction = get_use_case_prompt(use_case)
    audience_context = audience_insight or "Not specified"

    system_prompt = f"""
You are a world-class direct response copywriter. You're writing short, emotionally powerful headlines using classic persuasion frameworks.

Context:
- Audience: Australian share market investors
- Offer: A new report with expert ASX stock recommendations
- Use case: {use_case}
- Audience insight: {audience_context}

Instructions:
- Keep headlines bold, benefit-driven, and specific
- Avoid clichés like \"boost your portfolio\" or vague promises
- Each headline must match its framework’s logic and tone
- Do not reuse phrasing across frameworks
- Tone should match the use case — e.g. punchy for Facebook, clear for landing page
- Return only the rewritten headline
"""

    framework_prompts = {
        "AIDA": f"Rewrite the following headline using the AIDA framework (Attention, Interest, Desire, Action):\n\nOriginal headline: {input_headline}\nRewritten headline:",
        "PAS": f"Rewrite the following headline using the PAS framework (Problem, Agitate, Solution):\n\nOriginal headline: {input_headline}\nRewritten headline:",
        "BAB": f"Rewrite the following headline using the BAB framework (Before, After, Bridge):\n\nOriginal headline: {input_headline}\nRewritten headline:",
        "FAB": f"Rewrite the following headline using the FAB framework (Features, Advantages, Benefits):\n\nOriginal headline: {input_headline}\nRewritten headline:",
        "4 U’s": f"Rewrite the following headline using the 4 U’s framework (Urgent, Unique, Useful, Ultra-specific):\n\nOriginal headline: {input_headline}\nRewritten headline:",
        "5 P’s": f"Rewrite the following headline using the 5 P’s framework (Promise, Picture, Prove, Push, Personal):\n\nOriginal headline: {input_headline}\nRewritten headline:",
        "Persuasion Equation": f"Rewrite the following headline using the Persuasion Equation (Urgent Problem, Unique Promise, Unquestionable Proof, User-friendly Proposition):\n\nOriginal headline: {input_headline}\nRewritten headline:"
    }

    output = []
    for name, user_prompt in framework_prompts.items():
        try:
            new_headline = call_openai(system_prompt, user_prompt)
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
