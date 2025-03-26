import sys
import os
import pandas as pd
from langchain_core.documents import Document
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings


PROJECT_DIR = os.path.dirname(__file__)
ROOT_DIR = os.path.abspath(
    os.path.join(
        PROJECT_DIR,
        os.pardir,
        os.pardir
    )
)
DATA_DIR = os.path.abspath(
    os.path.join(
        PROJECT_DIR,
        "data"
    )
)
CHROMA_DB = os.path.abspath(
    os.path.join(
        PROJECT_DIR,
        "chroma_db"
    )
)

sys.path.extend([ROOT_DIR])

from src.backend.extract_meta_data import extract_meta_data, extract_documents

class VectorDB:
    def __init__(self, config):
        self.config = config
        self.data = None
        self.embeddings = HuggingFaceEmbeddings(model_name="Snowflake/snowflake-arctic-embed-m-long", model_kwargs={'trust_remote_code': True})
        self.documents = None
        self.vector_store = None

    def load_data(self):
        # Initialize an empty DataFrame to hold all data
        all_data = pd.DataFrame()

        # Iterate through all CSV files in the specified directory
        for file_name in os.listdir(self.config["data_directory"]):
            if file_name.endswith(".csv"):
                file_path = os.path.join(self.config["data_directory"], file_name)
                print(f"Loading data from: {file_path}")
                csv_data = pd.read_csv(file_path)
                all_data = pd.concat([all_data, csv_data], ignore_index=True)

        self.data = all_data

    def convert_to_documents(self):
        self.documents = [
            Document(
                page_content=extract_documents(row),
                metadata=extract_meta_data(row)
            )
            for _, row in self.data.iterrows()
        ]
        print("MADE ALL DOCUMENTS")
    
    def create_vector_store(self):
        self.load_data()
        self.convert_to_documents()
        self.vector_store = Chroma.from_documents(
            documents=self.documents,
            embedding=self.embeddings,
            persist_directory=self.config["persist_directory"]
        )
        print("CHROMA DB HAS BEEN CREATED")

if __name__ == "__main__":
    vectordb = VectorDB({
        "data_directory": DATA_DIR,
        "persist_directory": CHROMA_DB
    })
    vectordb.create_vector_store() 
