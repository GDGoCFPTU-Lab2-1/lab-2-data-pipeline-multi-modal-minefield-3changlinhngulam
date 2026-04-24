import pandas as pd
import re
from datetime import datetime

# ==========================================
# ROLE 2: ETL/ELT BUILDER
# ==========================================
# Task: Process sales records, handling type traps and duplicates.

def process_sales_csv(file_path):
    # --- FILE READING (Handled for students) ---
    df = pd.read_csv(file_path)
    # ------------------------------------------
    
    # Remove duplicate rows based on 'id'
    df = df.drop_duplicates(subset=['id'], keep='first')
    
    # Clean 'price' column: convert "$1200", "250000", "five dollars" to floats
    def clean_price(price_str):
        if pd.isna(price_str) or price_str in ['N/A', 'NULL', 'Liên hệ']:
            return None
        
        price_str = str(price_str).strip()
        
        # Handle text prices
        if 'five dollars' in price_str.lower():
            return 5.0
        
        # Remove $ and commas
        price_str = price_str.replace('$', '').replace(',', '')
        
        # Try to convert to float
        try:
            return float(price_str)
        except:
            return None
    
    df['price_cleaned'] = df['price'].apply(clean_price)
    
    # Normalize 'date_of_sale' into a single format (YYYY-MM-DD)
    def normalize_date(date_str):
        if pd.isna(date_str):
            return None
        
        date_str = str(date_str).strip()
        
        # Try different date formats
        formats = [
            '%Y-%m-%d',           # 2026-01-15
            '%d/%m/%Y',           # 15/01/2026
            '%d-%m-%Y',           # 17-01-2026
            '%Y/%m/%d',           # 2026/01/19
            '%d %b %Y',           # 19 Jan 2026
        ]
        
        for fmt in formats:
            try:
                dt = datetime.strptime(date_str, fmt)
                return dt.strftime('%Y-%m-%d')
            except:
                continue
        
        # Handle "January 16th 2026" or "January 22nd 2026"
        match = re.search(r'(\w+)\s+(\d+)(?:st|nd|rd|th)?\s+(\d{4})', date_str)
        if match:
            try:
                month_name, day, year = match.groups()
                dt = datetime.strptime(f"{month_name} {day} {year}", '%B %d %Y')
                return dt.strftime('%Y-%m-%d')
            except:
                pass
        
        return None
    
    df['date_normalized'] = df['date_of_sale'].apply(normalize_date)
    
    # Return a list of dictionaries for the UnifiedDocument schema
    documents = []
    for idx, row in df.iterrows():
        doc = {
            "document_id": f"csv-{row['id']}",
            "content": f"Sale Record: {row['product_name']} in {row['category']}, Price: {row['price']}, Date: {row['date_of_sale']}",
            "source_type": "CSV",
            "author": "Sales System",
            "timestamp": None,
            "tags": ["sales", "transaction", row['category'].lower()],
            "source_metadata": {
                "original_file": "sales_records.csv",
                "product_name": row['product_name'],
                "category": row['category'],
                "price_raw": str(row['price']),
                "price_cleaned": row['price_cleaned'],
                "currency": row['currency'],
                "date_raw": row['date_of_sale'],
                "date_normalized": row['date_normalized'],
                "seller_id": row['seller_id'],
                "stock_quantity": str(row['stock_quantity'])
            }
        }
        documents.append(doc)
    
    return documents

