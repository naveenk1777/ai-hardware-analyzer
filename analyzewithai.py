from google import genai
import os
from pydantic import BaseModel
import os

client=genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

class AIreport(BaseModel):
    fault_detected: bool
    fault_reason: str

def analyzewithai(telemetry_array:list)->AIreport:
    prompt=f"""
    You are a embeded systems diagnostic machine
    analyze the last 100 readings of {telemetry_array}
    if irstus is consistently true flag it as sensor blocked fault
    if battery is dropping too fast flag it as power failure
    """
    response=client.models.generate_content (
        model='gemini-2.5-flash',
        contents=prompt,
        config={
            'response_mime_type':'application/json',
            'response_schema':AIreport,
            'temperature':0.1
        }
    ) 
    
    return response.parsed
