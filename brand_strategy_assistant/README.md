# Brand Strategy AI Assistant

A multi-page AI-powered app for analyzing customer perception, brand communication and competition, strategic alignment — built with Streamlit, Transformers, ML Technics, and LLM APIs (OpenAI).

The app is hosted on Streamlit and can be viewed on:

https://brand-strategy-assistant.streamlit.app/

---

## Features

- Welcome Page
- Brand Analysis
- Customer Analysis
- Competitors Analysis
- AI-Powered Chatbot

### Customer Review Analysis Pipeline

- Customer reviews are scraped from google_play_scraper
- Extracts:
  - Main topics from user reviews:
    Derived by OpenAI for a 1000 uniform sample of reviews, modeled (utilizing XGBoost Classifier) for the rest
  - Sentiment classification (multilingual, model = 'tabularisai/multilingual-sentiment-analysis' from Hugging Face
- Maps reviews to psychological value categories (e.g., *trust*, *freedom*, *simplicity*, etc.)

### Brand Value Mapping

- Analyzes company brand content (extracted e.g. from their “About Us” page)
- Matches against value keywords (for further information, contact our specialists) to detect the brand positioning
- Compares against how users perceive the brand
- Compares against Klarna's competitors:
  supported_brands = ["Klarna", "N26", "Revolut", "Trade Republic", "Bunq"]

### Visual Insights

- Polar/radar charts for value alignment for each brand based on their positioning
- Polar/radar charts comparison of the brand with its competitors
- Polar/radar charts for value alignment for each brand based on user perception
- Heatmaps of sentiment vs topic per brand
- Sentiment analysis over time per brand per topic

### Agent Chatbot

- Ask brand strategy questions like:
  - "We see decline in new users, can you please tell us what is the current brand strategy and gaps in user perception for Klarna?"
  - "How can Klarna differentiate itself from Bunq to acquire more users?"
  - "We are planning a new brand marketing campaign for autumn and we would like to have a strategic direction and a breakdown on main    channels and messaging"
- Responses are generated using LLMs + preprocessed insights.

### Persistent Memory

- Chatbot remembers conversation across a session
