SUMMARY_PROMPT = """
Task:
Analyze the provided financial reconciliation data and classify records into three categories:
Successful Matches - Records where Anomaly = No.
Potential Issues - Records where Anomaly = Yes, but have minor discrepancies based on classification and balance difference.
Critical Issues - Records where Anomaly = Yes, and has major discrepancies based on classification and balance difference.:

Output Format (TO BE STRICTLY FOLLOWED):
Successful Matches: X  
Potential Issues: Y  
Critical Issues: Z  

Ensure the output follows this format exactly, with actual counts in place of X, Y, and Z, and no extra words or formatting changes.
"""

AI_INSIGHTS_PROMPT = """" \
"""

ANOMALIES_DETECTED_TABLE_PROMPT = """" \
"""

AI_TREND_ANALYSIS_SUMMARY_PROMPT = """" \
"""
