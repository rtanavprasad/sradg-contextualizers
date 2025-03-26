import os
import sys
import json
import time

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_chroma import Chroma
from langchain_huggingface.embeddings import HuggingFaceEmbeddings
from dotenv import load_dotenv, find_dotenv


PROJECT_DIR = os.path.dirname(__file__)
ROOT_DIR = os.path.abspath(
    os.path.join(
        PROJECT_DIR,
        os.pardir,
        os.pardir
    )
)
ENVKEY_DIRECTORY = os.path.abspath(
    os.path.join(
        ROOT_DIR,

    )
)

sys.path.extend([ROOT_DIR])

from src.backend.extract_details import SUMMARY_PROMPT, AI_INSIGHTS_PROMPT, AI_TREND_ANALYSIS_SUMMARY_PROMPT, ANOMALIES_DETECTED_TABLE_PROMPT
from src.backend.extract_details import format_response_summary, format_response_ai_insights, format_response_anomalies_table, format_response_trend_analysis
from src.backend.analyze import analyze_without_metadata

load_dotenv(find_dotenv())

gemini_api_key = os.getenv("GEMINI_API_KEY")
os.environ["GOOGLE_API_KEY"] = gemini_api_key

CACHE_FILE = "response_cache.json"

class Interface:
    def __init__(self):
        self.llm = ChatGoogleGenerativeAI(
            model="gemini-2.0-flash",
            convert_system_message_to_human=True,
            temperature=0.1,
            top_p=0.95,
            top_k=40,
            max_output_tokens=2048,
        )
        CHROMA_PATH = "./chroma_db"
        self.embedding_function = HuggingFaceEmbeddings(model_name="Snowflake/snowflake-arctic-embed-m-long", \
                                                    model_kwargs={'trust_remote_code': True})
        self.db = Chroma(persist_directory=CHROMA_PATH, embedding_function=self.embedding_function)

    def load_cache(self):
        if os.path.exists(CACHE_FILE):
            with open(CACHE_FILE, "r") as f:
                return json.load(f)
        return {}

    def save_cache(self, cache):
        with open(CACHE_FILE, "w") as f:
            json.dump(cache, f)

    def analyze_with_cache(self, llm, prompt, cache_key):
        cache = self.load_cache()
        if cache_key in cache:
            print(f"Using cached response for {cache_key}")
            return cache[cache_key]
        
        response = analyze_without_metadata(llm, prompt)
        cache[cache_key] = response
        self.save_cache(cache)
        return response

    # Example usage in the Interface class
    def analyze_CACHE(self):
        summary = self.analyze_with_cache(self.llm, SUMMARY_PROMPT, "summary")
        print("FINISHED SUMMARY")
        time.sleep(60)
        ai_insights = self.analyze_with_cache(self.llm, AI_INSIGHTS_PROMPT, "ai_insights")
        print("FINISHED INSIGHTS")
        time.sleep(60)
        anomalies_detected_table = self.analyze_with_cache(self.llm, ANOMALIES_DETECTED_TABLE_PROMPT, "anomalies_detected_table")
        print("FINISHED tables")
        time.sleep(60)
        ai_trend_analysis_summary = self.analyze_with_cache(self.llm, AI_TREND_ANALYSIS_SUMMARY_PROMPT, "ai_trend_analysis_summary")
        print(summary)
        print(ai_insights)
        print(anomalies_detected_table)
        print(ai_trend_analysis_summary)
        return {
            "summary": format_response_summary(summary),
            "Details": {
                "AIInsights": format_response_ai_insights(ai_insights),
                "AnomaliesDetectedTable": format_response_anomalies_table(anomalies_detected_table),
                "AITrendAnalysisSummary": format_response_trend_analysis(ai_trend_analysis_summary)
            }
        }
    
    def analyze(self):
        summary = analyze_without_metadata(self.llm, SUMMARY_PROMPT)
        print("FINISHED SUMMARY")
        time.sleep(60)
        ai_insights = analyze_without_metadata(self.llm, AI_INSIGHTS_PROMPT)
        print("FINISHED INSIGHTS")
        time.sleep(60)
        anomalies_detected_table = analyze_without_metadata(self.llm, ANOMALIES_DETECTED_TABLE_PROMPT)
        print("FINISHED tables")
        time.sleep(60)
        ai_trend_analysis_summary = analyze_without_metadata(self.llm, AI_TREND_ANALYSIS_SUMMARY_PROMPT)
        print(summary)
        print(anomalies_detected_table)
        print(ai_trend_analysis_summary)
        return {
            "summary": format_response_summary(summary),
            "Details": {
                "AIInsights": format_response_ai_insights(ai_insights),
                "AnomaliesDetectedTable": format_response_anomalies_table(anomalies_detected_table),
                "AITrendAnalysisSummary": format_response_trend_analysis(ai_trend_analysis_summary)
            }
        }
    
if __name__ == "__main__":
    print(ROOT_DIR)
    load_dotenv(find_dotenv(ROOT_DIR))
    interface = Interface()

    answers = interface.analyze_CACHE()
    print(answers)