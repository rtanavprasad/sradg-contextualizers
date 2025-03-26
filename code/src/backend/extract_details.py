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

THE RESPONSE SHOULD STRICTLY ONLY CONTAIN THE 3 LINES OF THE OUTPUT STRUCTURE
"""

AI_INSIGHTS_PROMPT = """
Based on the current Anomalies detected in the data, give a list of all remediations that can be done in the data to ensure successful reconciliation.

Output Format (TO BE STRICTLY FOLLOWED):
--<start_response>--
1. Remediation 1
2. Remediation 2
3. Remediation 3
--<end_response>--

Ensure the output follows this format exactly, with each remediation on a new line, numbered, and no extra words or formatting changes.

the fields <start_response> and <end_response> Must not be changed or removed.

THE RESPONSE SHOULD NOT CONTAIN MORE THAN 3 REMEDIATIONS.
"""

ANOMALIES_DETECTED_TABLE_PROMPT = """"
List all the records with anomalies detected in the data, and provide the data entries in the following format.

Output Format (TO BE STRICTLY FOLLOWED):
--<start_response>--
<table> <thead> <tr> <th>Hourly Date Time</th> <th>Account Number</th> <th>BranchAU</th> <th>GL Balance</th> <th>Ihub Balance</th> <th>Anomaly Type</th> <th>AI Comment</th> <th>Actions</th> </tr> </thead> 
<tbody>
<tr> <td>DateTime1</td> <td>AccountNumber1</td> <td>BranchAU1</td> <td>GLBalance1</td> <td>IhubBalance1</td> <td><span class="anomaly-type type-mismatch">Status Mismatch</span></td> <td>AIComment1</td> <td><button class="btn btn-outline" style="padding: 4px 8px; font-size: 12px;"> <i class="fas fa-comment"></i> Feedback </button></td> </tr>
<tr> <td>DateTime2</td> <td>AccountNumber2</td> <td>BranchAU2</td> <td>GLBalance2</td> <td>IhubBalance2</td> <td><span class="anomaly-type type-mismatch">Status Mismatch</span></td> <td>AIComment2</td> <td><button class="btn btn-outline" style="padding: 4px 8px; font-size: 12px;"> <i class="fas fa-comment"></i> Feedback </button></td> </tr>
--<end_response>--

Ensure the output follows this format exactly.

LIST 5 RECORDS AT MAXIMUM.
"""

AI_TREND_ANALYSIS_SUMMARY_PROMPT = """"
Analyze the entire data and provide the trend analysis summary for the given data.

A sample answer might be - The anomalies show a weekly pattern with peaks on Mondays. 68% of value mismatches occur within 2 hours of system synchronization. Missing data anomalies have decreased by 24% since last month's process improvements.

OUTPUT FORMAT:
--<start_response>--
Trend Analysis Summary Text
--<end_response>--

Ensure the output follows this format exactly.In the Output Response, the fields --<start_response>-- and --<end_response>-- MUST not be changed or removed.
"""

def format_response_summary(response):
    # Split the response into lines
    lines = response.strip().split("\n")
    
    # Parse each line and extract the counts
    result = {}
    for line in lines:
        if line.startswith("Successful Matches:"):
            result["success"] = int(line.split(":")[1].strip())
        elif line.startswith("Potential Issues:"):
            result["PotentialIssue"] = int(line.split(":")[1].strip())
        elif line.startswith("Critical Issues:"):
            result["CriticalIssue"] = int(line.split(":")[1].strip())
    
    return result

def format_response_ai_insights(response):
    # Extract the content between <start_response> and <end_response>
    start_tag = "--<start_response>--"
    end_tag = "--<end_response>--"
    
    # Find the start and end indices
    start_index = response.find(start_tag) + len(start_tag)
    end_index = response.find(end_tag)
    
    # Extract the content between the tags
    if start_index != -1 and end_index != -1:
        content = response[start_index:end_index].strip()
    else:
        return []  # Return an empty list if tags are not found
    
    # Split the content into lines and clean up
    insights = [line.strip() for line in content.split("\n") if line.strip()]
    
    return ["Based on historical data and current anomalies, the AI suggests:", ""] + insights

def format_response_anomalies_table(response):
    # Extract the content between <start_response> and <end_response>
    start_tag = "--<start_response>--"
    end_tag = "--<end_response>--"
    
    # Find the start and end indices
    start_index = response.find(start_tag) + len(start_tag)
    end_index = response.find(end_tag)
    
    # Extract the content between the tags
    if start_index != -1 and end_index != -1:
        content = response[start_index:end_index].strip()
    else:
        return ""  # Return an empty string if tags are not found
    
    # Remove line breaks and return the content as a single line
    single_line_content = " ".join(content.split())
    return single_line_content

def format_response_trend_analysis(response):
    # Extract the content between <start_response> and <end_response>
    start_tag = "--<start_response>--"
    end_tag = "--<end_response>--"
    
    # Find the start and end indices
    start_index = response.find(start_tag) + len(start_tag)
    end_index = response.find(end_tag)
    
    # Extract the content between the tags
    if start_index != -1 and end_index != -1:
        content = response[start_index:end_index].strip()
    else:
        return ""  # Return an empty string if tags are not found
    
    # Return the extracted content as a single line
    single_line_content = " ".join(content.split())
    return single_line_content

if __name__ == "__main__":
    response = """Successful Matches: 120  
Potential Issues: 45  
Critical Issues: 10"""
    ai_response = """<start_response>
1. Remediation 1
2. Remediation 2
3. Remediation 3
<end_response>"""
    table = """--<start_response>--
<table> <thead> <tr> <th>Hourly Date Time</th> <th>Account Number</th> <th>BranchAU</th> <th>GL Balance</th> <th>Ihub Balance</th> <th>Anomaly Type</th> <th>AI Comment</th> <th>Actions</th> </tr> </thead> 
<tbody>
<tr> <td>2025-01-01 00:00</td> <td>1</td> <td>1</td> <td>4925.066925</td> <td>5041.991391</td> <td>Balance turned negative</td> <td>Check GL Balance</td> <td>Investigate</td> </tr>
<tr> <td>2025-01-01 01:00</td> <td>2</td> <td>2</td> <td>2393.724499</td> <td>3285.474283</td> <td>Sudden spike</td> <td>Review transactions</td> <td>Escalate</td> </tr>
</tbody>
</table>
--<end_response>--"""
    trend_analysis_response = """<start_response>
The anomalies show a weekly pattern with peaks on Mondays. 68% of value mismatches occur within 2 hours of system synchronization. Missing data anomalies have decreased by 24% since last month's process improvements.
<end_response>"""
    
    print(format_response_trend_analysis(trend_analysis_response))
    print(format_response_summary(response))
    print(format_response_ai_insights(ai_response))
    print(format_response_anomalies_table(table))