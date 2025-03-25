from langchain_core.prompts import PromptTemplate
from langchain_huggingface import HuggingFaceEndpoint

PROMPT = """

"""

def extract_meta_data(row):
    metadata = {
        "Hourly Date Time": row["Hourly Date Time"],
        "Account Number": row["Account Number"],
        "Anomaly": row["Anomaly"],
        "GL Balance": row["GL Balance"],
        "Ihub Balance": row["Ihub Balance"],
        "Difference": row["difference"],
        "Branch AU": row["BranchAU"],
        "Company Code": row["CompanyCode"],
    }
    return metadata

def extract_documents(row):
    page_content=(
            f"At {row['Hourly Date Time']}, account {row['Account Number']} in branch {row['BranchAU']} "
            f"and company {row['CompanyCode']} had a classification of '{row['Classification']}'. "
            f"The anomaly status is '{row['Anomaly']}'. The GL Balance was {row['GL Balance']}, "
            f"the Ihub Balance was {row['Ihub Balance']}, and the difference was {row['difference']}."
        )
    return page_content