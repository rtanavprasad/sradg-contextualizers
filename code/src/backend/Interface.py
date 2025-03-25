import os
import sys

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_chroma import Chroma
from langchain_huggingface.embeddings import HuggingFaceEmbeddings
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv

from extract_details import SUMMARY_PROMPT
from analyze import analyze_without_metadata

PROJECT_DIR = os.path.dirname(__file__)
ROOT_DIR = os.path.abspath(
    os.path.join(
        PROJECT_DIR,
        os.pardir,
        os.pardir
    )
)

sys.path.extend([ROOT_DIR])

gemini_api_key = os.getenv("GEMINI_API_KEY")
os.environ["GOOGLE_API_KEY"] = gemini_api_key

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
        CHROMA_PATH = "./chroma"
        self.embedding_function = HuggingFaceEmbeddings(model_name="Snowflake/snowflake-arctic-embed-m-long", \
                                                    model_kwargs={'trust_remote_code': True})
        self.db = Chroma(persist_directory=CHROMA_PATH, embedding_function=self.embedding_function)
    
    def analyze(self, QUERY):
        # Output format
        # data = {
        #     "summary" : {
        #         "success": "1,245",
        #         "PotentialIssue": "42",
        #         "CriticalIssue": "18"
        #     },
        #     "Details": {
        #         "AIInsights": [
        #             "Based on historical data and current anomalies, the AI suggests:",
        #             "",
        #             "1. Implement a 15-minute delay in reconciliation for new transactions to account for processing time.",
        #             "2. Create an exception rule for status changes that occur between 2-3 AM during maintenance windows.",
        #             "3. 82% of currency mismatches involve EUR-USD pairs - consider adding automatic conversion verification."
        #         ],
        #         "AnomaliesDetectedTable": '<table> <thead> <tr> <th>ID</th> <th>Key Value</th> <th>Source 1 Value</th> <th>Source 2 Value</th> <th>Anomaly Type</th> <th>AI Comment</th> <th>Actions</th> </tr> </thead> <tbody> <tr> <td>#1001</td> <td>TXN-2023-0456</td> <td>$1,250.00</td> <td>$1,200.00</td> <td><span class="anomaly-type type-mismatch">Value Mismatch</span></td> <td>Amount difference detected. Possible fee deduction in source 2.</td> <td> <button class="btn btn-outline" style="padding: 4px 8px; font-size: 12px;"> <i class="fas fa-comment"></i> Feedback </button> </td> </tr> <tr> <td>#1002</td> <td>CUST-78945</td> <td>Active</td> <td>Inactive</td> <td><span class="anomaly-type type-mismatch">Status Mismatch</span></td> <td>Customer status differs between systems. Check update timing.</td> <td> <button class="btn btn-outline" style="padding: 4px 8px; font-size: 12px;"> <i class="fas fa-comment"></i> Feedback </button> </td> </tr> <tr> <td>#1003</td> <td>ORD-45612</td> <td>5 items</td> <td>Missing</td> <td><span class="anomaly-type missing-data">Missing Data</span></td> <td>Order not found in source 2. Possible synchronization delay.</td> <td> <button class="btn btn-outline" style="padding: 4px 8px; font-size: 12px;"> <i class="fas fa-comment"></i> Feedback </button> </td> </tr> <tr> <td>#1004</td> <td>TXN-2023-0789</td> <td>USD</td> <td>EUR</td> <td><span class="anomaly-type type-mismatch">Currency Mismatch</span></td> <td>Different currencies detected. Check FX conversion process.</td> <td> <button class="btn btn-outline" style="padding: 4px 8px; font-size: 12px;"> <i class="fas fa-comment"></i> Feedback </button> </td> </tr> </tbody> </table>',
        #         "AITrendAnalysisSummary": "The anomalies show a weekly pattern with peaks on Mondays. 68% of value mismatches occur within 2 hours of system synchronization. Missing data anomalies have decreased by 24% since last month's process improvements."
        #     }
        # }

        summary = analyze_without_metadata(self.llm, QUERY)
        print(summary)

if __name__ == "__main__":
    load_dotenv()
    interface = Interface()

    interface.analyze(QUERY=SUMMARY_PROMPT)