import pandas as pd
from langchain_core.documents import Document
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings

from extract_meta_data import extract_meta_data, extract_documents

class VectorDB:
    def __init__(self, config):
        self.config = config
        self.data = None
        self.embeddings = HuggingFaceEmbeddings(model_name="Snowflake/snowflake-arctic-embed-m-long", model_kwargs={'trust_remote_code': True})
        self.documents = None
        self.vector_store = None

    def load_data(self):
        csv_file = self.config["data_path"]
        self.data = pd.read_csv(csv_file)

    def convert_to_documents(self):
        self.documents = [
            Document(
                page_content=extract_documents(row),
                metadata=extract_meta_data(row)
            )
            for _, row in self.data.iterrows()
        ]
    
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
        "data_path": "data/sample.csv",
        "persist_directory": "./chroma_db"
    })
    vectordb.create_vector_store()
