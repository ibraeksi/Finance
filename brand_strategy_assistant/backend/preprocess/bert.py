from bertopic import BERTopic
from bertopic.representation import OpenAI, KeyBERTInspired, MaximalMarginalRelevance
import pandas as pd
# from utils.params import *

# client = openai.OpenAI(api_key=api_key)

class BERTTopic:
    def __init__(self, docs, client=None, language="multilingual", min_topic_size=3):
        """
        Initialize the class with documents and common settings.
        """
        self.docs = docs
        self.client = client
        self.language = language
        self.min_topic_size = min_topic_size
        self.results_df = pd.DataFrame({"content": docs})

    def openai(self):
        """
        BERTopic using OpenAI GPT-based topic representation model.
        """
        if self.client is None:
            raise ValueError("OpenAI client must be provided for OpenAI-based topic modeling.")

        openai_model = OpenAI(client=self.client, model="gpt-4o", chat=True)
        topic_model = BERTopic(
            language=self.language,
            representation_model=openai_model,
            min_topic_size=self.min_topic_size
        )
        topics, _ = topic_model.fit_transform(self.docs)
        self.results_df["OpenAI_topic_id"] = topics
        self.results_df["OpenAI_topic_keywords"] = [topic_model.get_topic(t) for t in topics]

    def keybert(self):
        """
        BERTopic using KeyBERT model representation.
        """
        keybert_model = KeyBERTInspired()
        topic_model = BERTopic(
            language=self.language,
            representation_model=keybert_model,
            min_topic_size=self.min_topic_size
        )
        topics, _ = topic_model.fit_transform(self.docs)
        self.results_df["KeyBERT_topic_id"] = topics
        self.results_df["KeyBERT_topic_keywords"] = [topic_model.get_topic(t) for t in topics]

    def mmr(self):
        """
        BERTopic using Maximal Marginal Relevance (MMR) representation model.
        """
        mmr_model = MaximalMarginalRelevance(diversity=0.3)
        topic_model = BERTopic(
            language=self.language,
            representation_model=mmr_model,
            min_topic_size=self.min_topic_size
        )
        topics, _ = topic_model.fit_transform(self.docs)
        self.results_df["MMR_topic_id"] = topics
        self.results_df["MMR_topic_keywords"] = [topic_model.get_topic(t) for t in topics]

    def get_results(self):
        return self.results_df
