from langchain.chains import RetrievalQA
from langchain.llms import HuggingFacePipeline
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from transformers import pipeline
from langchain_google_genai import ChatGoogleGenerativeAI

import os

# Initialize HuggingFace embeddings (same as used during creation)
embeddings = HuggingFaceEmbeddings(model_name="Snowflake/snowflake-arctic-embed-m-long", model_kwargs={'trust_remote_code': True})

# Load the persisted ChromaDB
vectorstore = Chroma(
    persist_directory="./chroma_db",  # Directory where the ChromaDB is stored
    embedding_function=embeddings
)

# Inspect all documents and metadata in the ChromaDB
# all_docs = vectorstore._collection.get(include=["metadatas", "documents"])

# record_count = vectorstore._collection.count()
# print(f"Total number of records in ChromaDB: {record_count}")



# Set up the retriever
retriever = vectorstore.as_retriever(search_type="similarity", 
                                     search_kwargs={"k": 1000})
                                    #  filter=lambda metadata: metadata["Anomaly"] == "Yes")

# Initialize the Gemini LLM using HuggingFacePipeline
# hf_pipeline = pipeline("text-generation", model="google/gemma-7b", max_length=512)  # Replace "Gemini-1" with the correct model name
# llm = HuggingFacePipeline(pipeline=hf_pipeline)

gemini_api_key = os.getenv("GEMINI_API_KEY")
os.environ["GOOGLE_API_KEY"] = gemini_api_key

llm = ChatGoogleGenerativeAI(
      model="gemini-2.0-flash",
      convert_system_message_to_human=True,
      temperature=0.1,
      top_p=0.95,
      top_k=40,
      max_output_tokens=2048,
   )

# Create a RetrievalQA chain
qa_chain = RetrievalQA.from_chain_type(
    llm=llm,
    retriever=retriever,
    return_source_documents=True
)

# Query the vector database
query = "Give total count of records with anomaly as Yes."
result = qa_chain({"query": query})

# Print the response
print("Answer:", result["result"])

# Print the source documents
# print("\nSource Documents:")
# for doc in result["source_documents"]:
#     print(f"- {doc.page_content} (Metadata: {doc.metadata})")