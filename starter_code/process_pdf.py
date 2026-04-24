from openai import OpenAI
import os
import json
from dotenv import load_dotenv
from PyPDF2 import PdfReader

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def extract_pdf_data(file_path):
    if not os.path.exists(file_path):
        print(f"Error: File not found at {file_path}")
        return None
    
    print(f"Reading PDF file: {file_path}")
    try:
        # Extract text from PDF using PyPDF2
        reader = PdfReader(file_path)
        pdf_text = ""
        for page in reader.pages:
            pdf_text += page.extract_text() + "\n"
        
        if not pdf_text.strip():
            print("Warning: No text extracted from PDF")
            return None
            
    except Exception as e:
        print(f"Failed to read PDF file: {e}")
        return None
        
    prompt = f"""
Analyze this document text and extract a summary and the author. 
Output exactly as a JSON object matching this exact format:
{{
    "document_id": "pdf-doc-001",
    "content": "Summary: [Insert your 3-sentence summary here]",
    "source_type": "PDF",
    "author": "[Insert author name here]",
    "timestamp": null,
    "source_metadata": {{"original_file": "lecture_notes.pdf"}}
}}

Document text:
{pdf_text[:4000]}
"""
    
    print("Generating content from PDF using OpenAI...")
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            max_tokens=1000
        )
        content_text = response.choices[0].message.content
    except Exception as e:
        print(f"Failed to process PDF with OpenAI: {e}")
        return None
    
    # Simple cleanup if the response is wrapped in markdown json block
    if content_text.startswith("```json"):
        content_text = content_text[7:]
    if content_text.endswith("```"):
        content_text = content_text[:-3]
    if content_text.startswith("```"):
        content_text = content_text[3:]
        
    extracted_data = json.loads(content_text.strip())
    return extracted_data
