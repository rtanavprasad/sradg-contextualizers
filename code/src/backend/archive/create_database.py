import pandas as pd
from langchain_core.documents import Document
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings

csv_file = "data/sample.csv"
df = pd.read_csv(csv_file)

embeddings = HuggingFaceEmbeddings(model_name="Snowflake/snowflake-arctic-embed-m-long", model_kwargs={'trust_remote_code': True})

# Convert CSV rows into LangChain Document objects
# Convert CSV rows into LangChain Document objects
documents = [
    Document(
        page_content=(
            f"At {row['Hourly Date Time']}, account {row['Account Number']} in branch {row['BranchAU']} "
            f"and company {row['CompanyCode']} had a classification of '{row['Classification']}'. "
            f"The anomaly status is '{row['Anomaly']}'. The GL Balance was {row['GL Balance']}, "
            f"the Ihub Balance was {row['Ihub Balance']}, and the difference was {row['difference']}."
        ),
        metadata={
            "Hourly Date Time": row["Hourly Date Time"],
            "Account Number": row["Account Number"],
            "BranchAU": row["BranchAU"],
            "CompanyCode": row["CompanyCode"],
            "Anomaly": row["Anomaly"],
            "GL Balance": row["GL Balance"],
            "Ihub Balance": row["Ihub Balance"],
            "Difference": row["difference"],
            "Classification": row["Classification"],
        }
    )
    for _, row in df.iterrows()
]

# Create a ChromaDB vector store
vectorstore = Chroma.from_documents(
    documents=documents,
    embedding=embeddings,
    persist_directory="./chroma_db"  # Directory to store the database
)

print("ChromaDB has been created and saved!")