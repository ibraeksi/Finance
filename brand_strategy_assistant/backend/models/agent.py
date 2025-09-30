import pandas as pd
from pathlib import Path

user_reviews_sentiment_data = Path(__file__).parents[2] / 'data/preprocessed/final_reviews_with_topics_and_sentiment.csv'
user_reviews_sentiment_df=pd.read_csv(user_reviews_sentiment_data)

from openai import OpenAI
from backend.preprocess.alignment_score import get_alignment_summary
import json
from backend.package.sentiment_trends import get_monthly_sentiment_trends
import streamlit as st

# Check if user chose a brand, if not default to Klarna
if 'chosen_brand' in st.session_state.keys():
    brand_name = st.session_state['chosen_brand']
else:
    brand_name = 'Klarna'

def system_prompt(brand_name):
    return f"""
You are a senior brand strategy AI assistant advising brand {brand_name} on marketing, advertising, and brand management.
Your role is to help {brand_name} win in the competitive fintech landscape by sharpening its brand positioning, communication strategy, and campaign messaging.
You always act in {brand_name}’s best interest. Your recommendations are designed to help Klarna stand out from competitors and better connect with customers.


You represent this {brand_name}’s interests and your role is to help them win customer attention, trust, and loyalty — especially in a highly competitive landscape. Your goal is to sharpen their brand identity, differentiate them from competitors, and align their messaging with what customers truly value.

You are operating in the German market, and your main competitors are: "N26", "Revolut", "Trade Republic", "Bunq"

You make recommendations based on three inputs:
1. The {brand_name}’s current brand positioning (messaging, values, tone)
2. Competitor positioning (where other brands overlap or stand out)
3. Customer perception (what users care about, as seen in reviews)

---


Available Tool:
You can call `get_alignment_summary(brand)` to:
- Compute a similarity or alignment score between brand and user values
- See the top brand-stated values vs top user-perceived values
- Identify gaps where the brand is over- or under-communicating
- Get a recommendation on what to reinforce or shift


You can call `get_monthly_sentiment_trends()` to:
- View sentiment development over time for each topic and brand
- Analyze average monthly sentiment (Bayesian-smoothed) across 12 months
- Spot patterns in customer sentiment by topic (e.g., declining trust, growing positivity around innovation)
- Detect changes in perception in last THREE months that might suggest brand fatigue, success, or unmet expectations. Be awa


---


Your Goals:
When asked about a brand’s strategy, perception, values, or ideas for campaigns:
1. **Analyze Data Sources**
   - Use `get_alignment_summary(brand)` to understand brand-user value alignment. But DO NOT provide the alignment scores to the user.
   - Use `get_monthly_sentiment_trends()` to assess how customers emotionally respond to each value over time.
   - Use `brand_compare_info` dictionary that provides you with additional input i.e. brands about us and results from the other analyses.
   - Use `brand_text` that provides you with a messaging written by the neobanks and their brand teams.


2. **Diagnose the Situation**
   Identify and highlight:
   - Values where the brand and users are **misaligned**
   - **Overused** or **under-recognized** themes
   - **Overlaps** with competitors (non-differentiating values)
   - Strategic risks or opportunities
   - Shifts in customer perception over time

3. **Recommend Strategic Actions**
Provide actionable guidance on:
   - **Messaging focus** — which values to **amplify**, **reframe**, or **soften**
   - **Tone and content themes** that better reflect user expectations
   - **Channels** and **formats** suited to reinforce key values (e.g., partnerships, UX, campaigns)
   - **Positioning statements** or tagline directions grounded in data
   - **How Klarna can differentiate itself from Revolut, N26, bunq, and Trade Republic

Provide reasoning for your suggestions, explaining the competitive advantage brand has in the market and the main misalignment gaps and white spaces in the values it can fill compared to competition.

When replying:

1. If response_stage == "summary" and it's the first-time question:
   - Provide only high-level diagnosis (3-4 bullet points max).
   - End by asking if the user wants a deeper analysis.
2. If response_stage == "deep_dive":
   - Provide trend analysis, data breakdown, strategic risks.
   - End by asking if user wants specific campaign ideas.
3. If response_stage == "strategy":
   - Provide actionable campaign, UX, product, and messaging suggestions.
   - Do not repeat diagnosis. Focus only on strategic actions.


If the input is vague or just a brand name, ask a clarifying question first instead of launching into a full report.
You should give full strategic guidance if asked directly about alignment, campaigns, or differentiation.

When evaluating sentiment, prioritize direction and change, not just overall averages. A brand that scores highly but is declining in recent months may be at risk of losing relevance or customer satisfaction.
A consistently strong perception in the past (e.g., for user_centricity) does not guarantee continued strength. A downward trend, especially sustained over recent months, may indicate growing dissatisfaction or shifts in expectations.
Therefore, even if a topic used to be positively perceived, a recent decline is a red flag — suggesting erosion of trust or relevance that needs immediate attention.

Avoid speculations, only ground your replies on the available data. Never guess an alignment - always call the tools first. Be concise but insightful. Sound like a confident strategist with access to real behavioral data — not just abstract theory. Think like a brand strategist sitting inside the {brand_name}’s team — focused, competitive, and customer-aware. You are clear, confident, and helpful.
"""


supported_brands = ["Klarna", "N26", "Revolut", "Trade Republic", "Bunq"]

def extract_brand_names(text: str, brand_list=None):
    if brand_list is None:
        brand_list = supported_brands
    text_lower = text.lower()
    extracted_brand = [brand for brand in brand_list if brand.lower() in text_lower]
    return extracted_brand


def handle_query(question: str, brand_kw_df, review_kw_df, api_key, chat_history=None, last_brands=None): # history: list[dict],
    client = OpenAI(api_key=api_key)

    if chat_history is None:
        chat_history = []

    brands = extract_brand_names(question)
    #print(brands)

    if not brands and last_brands:
        brands = last_brands

    if not brands:
        return f"Sorry, I couldn't find any known brands in your question. Supported brands: {', '.join(supported_brands)}."

    #if len(question.split()) < 4:
        #return "Tell me what can I help you with: messaging, user perception, or campaign ideas?"

    # elif len(brands) == 1:
    #     brand = brands[0]
    #     st.session_state.last_brands = brands
        #summary = get_alignment_summary(brand, brand_kw_df, review_kw_df)
        #sentiment_df = get_monthly_sentiment_trends(user_reviews_sentiment_df)
        #summary["sentiment"] = sentiment_df[sentiment_df["brand"].str.lower() == brand.lower()].to_dict(orient="records")

        #context = (
            #f"You are analyzing the brand alignment for {brand}.\n"
            #f"Use the JSON summary below to understand user perception vs brand values and generate strategy insights.\n\n"
            #f"Do not list recommendations or action steps yet.\n"
            #f"End by asking if the user would like a deeper breakdown with suggestions.\n\n"
            #f"{json.dumps(summary, indent=2)}"
        #)

        #prompt = (
            #f"You are a brand strategy consultant.\n\n"
            #f"User asked: \"{question}\"\n\n"
            #f"Use the summary below to answer with strategic recommendations:\n\n"
            #f"{context}"
        #)
    #     if "brand_summary" not in st.session_state:
    #         summary = get_alignment_summary(brand, brand_kw_df, review_kw_df)
    #         sentiment_df = get_monthly_sentiment_trends(user_reviews_sentiment_df)
    #         summary["sentiment"] = sentiment_df[sentiment_df["brand"].str.lower() == brand.lower()].to_dict(orient="records")
    #         st.session_state.brand_summary = summary
    #         st.session_state.response_stage = "summary"
    #     else:
    #         summary = st.session_state.brand_summary

    #     # Format summary for system-level context (only added once)
    #     if not any("brand_summary:" in m["content"] for m in chat_history):
    #         summary_msg = {
    #             "role": "system",
    #             "content": f"brand_summary:\n{json.dumps(summary, indent=2)}"
    #         }
    #         chat_history.insert(0, summary_msg)

    # elif len(brands) == 2:
    #     b1, b2 = brands
    #     st.session_state.last_brands = brands
    #     #summary1 = get_alignment_summary(b1, brand_kw_df, review_kw_df)
    #     #summary2 = get_alignment_summary(b2, brand_kw_df, review_kw_df)

    #     #sentiment_df = get_monthly_sentiment_trends(user_reviews_sentiment_df)
    #     #summary1["sentiment"] = sentiment_df[sentiment_df["brand"].str.lower() == b1.lower()].to_dict(orient="records")
    #     #summary2["sentiment"] = sentiment_df[sentiment_df["brand"].str.lower() == b2.lower()].to_dict(orient="records")

    #     #context = json.dumps({
    #     #    b1: summary1,
    #     #    b2: summary2
    #     #}, indent=2)


    #     #prompt = (
    #     #    f"You are a brand strategist comparing two brands.\n\n"
    #     #    f"User asked: \"{question}\"\n\n"
    #     #    f"Use the summaries below to compare their alignment with user perception."
    #     #    f"Highlight key differences and suggest which brand is better positioned:\n\n"
    #     #    f"{context}"
    #     #)

    #     if "brand_summary" not in st.session_state:
    #         summary1 = get_alignment_summary(b1, brand_kw_df, review_kw_df)
    #         summary2 = get_alignment_summary(b2, brand_kw_df, review_kw_df)
    #         sentiment_df = get_monthly_sentiment_trends(user_reviews_sentiment_df)
    #         summary1["sentiment"] = sentiment_df[sentiment_df["brand"].str.lower() == b1.lower()].to_dict(orient="records")
    #         summary2["sentiment"] = sentiment_df[sentiment_df["brand"].str.lower() == b2.lower()].to_dict(orient="records")
    #         combined = {b1: summary1, b2: summary2}
    #         st.session_state.brand_summary = combined
    #         st.session_state.response_stage = "summary"
    #     else:
    #         combined = st.session_state.brand_summary

    #     if not any("brand_summary:" in m["content"] for m in chat_history):
    #         chat_history.insert(0, {
    #             "role": "system",
    #             "content": f"brand_summary:\n{json.dumps(combined, indent=2)}"
    #         })

    # else:
    #     return "I can only compare up to two brands at a time. Please ask about one or two brands."
    new_brands = tuple(sorted(brands))
    last_loaded = st.session_state.get("loaded_brand_summary_for", ())

    if new_brands != last_loaded:
        if len(new_brands) == 1:
            brand = new_brands[0]
            summary = get_alignment_summary(brand, brand_kw_df, review_kw_df)
            sentiment_df = get_monthly_sentiment_trends(user_reviews_sentiment_df)
            summary["sentiment"] = sentiment_df[sentiment_df["brand"].str.lower() == brand.lower()].to_dict(orient="records")
            st.session_state.brand_summary = summary
        elif len(new_brands) == 2:
            b1, b2 = new_brands
            summary1 = get_alignment_summary(b1, brand_kw_df, review_kw_df)
            summary2 = get_alignment_summary(b2, brand_kw_df, review_kw_df)
            sentiment_df = get_monthly_sentiment_trends(user_reviews_sentiment_df)
            summary1["sentiment"] = sentiment_df[sentiment_df["brand"].str.lower() == b1.lower()].to_dict(orient="records")
            summary2["sentiment"] = sentiment_df[sentiment_df["brand"].str.lower() == b2.lower()].to_dict(orient="records")
            st.session_state.brand_summary = {b1: summary1, b2: summary2}
        else:
            return "I can only compare up to two brands at a time. Please ask about one or two brands."

        st.session_state.loaded_brand_summary_for = new_brands
        st.session_state.last_brands = brands
        st.session_state.response_stage = "summary"

    # Load summary for prompt generation
    summary = st.session_state.brand_summary
    brand_name = brands[0] if len(brands) == 1 else ', '.join(brands)
    brand_context = json.dumps(summary, indent=2)

    # Construct system prompt with dynamic brand + context
    sys_prompt = system_prompt(brand_name) + f"\n\nBRAND_CONTEXT:\n{brand_context}"

    # Send to OpenAI

    messages = [{"role": "system", "content": system_prompt(sys_prompt )}] + chat_history + [{"role": "user", "content": question}]

    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=messages,
            temperature=0.5
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error generating response: {str(e)}"
