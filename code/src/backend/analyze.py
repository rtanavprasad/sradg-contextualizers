from langchain.chains import RetrievalQA
from langchain_core.prompts import PromptTemplate
from langchain.retrievers.self_query.base import SelfQueryRetriever
from langchain_community.query_constructors.chroma import ChromaTranslator
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
 
embeddings = HuggingFaceEmbeddings(model_name="Snowflake/snowflake-arctic-embed-m-long", model_kwargs={'trust_remote_code': True})

# Load the persisted ChromaDB
vectorstore = Chroma(
    persist_directory="./chroma_db",  # Directory where the ChromaDB is stored
    embedding_function=embeddings
)

retriever = vectorstore.as_retriever(search_type="similarity", 
                                     search_kwargs={"k": 8000})

def analyze_without_metadata(llm, QUERY):
    
    qa_chain = RetrievalQA.from_chain_type(
                llm=llm,
                retriever=retriever,
                return_source_documents=True
            )

    # Query the vector database
    result = qa_chain({"query": QUERY})

    return result['result']