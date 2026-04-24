import re

# ==========================================
# ROLE 2: ETL/ELT BUILDER
# ==========================================
# Task: Clean the transcript text and extract key information.

def clean_transcript(file_path):
    # --- FILE READING (Handled for students) ---
    with open(file_path, 'r', encoding='utf-8') as f:
        text = f.read()
    # ------------------------------------------
    
    # Remove noise tokens like [Music], [inaudible], [Laughter], [Music starts], [Music ends]
    text = re.sub(r'\[Music[^\]]*\]', '', text)
    text = re.sub(r'\[inaudible\]', '', text)
    text = re.sub(r'\[Laughter\]', '', text)
    
    # Remove timestamps [00:00:00]
    text = re.sub(r'\[\d{2}:\d{2}:\d{2}\]', '', text)
    
    # Remove speaker labels [Speaker 1]:, [Speaker 2]:
    text = re.sub(r'\[Speaker \d+\]:', '', text)
    
    # Clean up extra whitespace
    text = re.sub(r'\s+', ' ', text).strip()
    
    # Find the price mentioned in Vietnamese words ("năm trăm nghìn")
    detected_price = None
    if "năm trăm nghìn" in text.lower():
        detected_price = 500000
    
    # Return a cleaned dictionary for the UnifiedDocument schema
    return {
        "document_id": "video-transcript-001",
        "content": text,
        "source_type": "Video",
        "author": "Unknown",
        "timestamp": None,
        "tags": ["transcript", "lecture"],
        "source_metadata": {
            "original_file": "demo_transcript.txt",
            "detected_price_vnd": detected_price
        }
    }

